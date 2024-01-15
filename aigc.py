import os
from typing import List, Dict
from openai import OpenAI
from dotenv import load_dotenv



class Aigc:
    def __init__(self) -> None:
        # Use environment variable for API key
        load_dotenv()

        # Get the API key from the environment variable
        api_key = os.getenv("OPENAI_API_KEY")
        print(api_key)

        self.client = OpenAI(
            api_key=api_key
        )

    def create_completion(self, question):
        try:
            response = self.client.completions.create(
                model="gpt-3.5-turbo-instruct", prompt=question, max_tokens=50
            )
            if response.choices:
                return response.choices[0].text.strip()
            else:
                return "No response from the AI model."
        except Exception as e:
            return f"An error occurred: {str(e)}"


class AlergyAI:
    def __init__(self) -> None:
        self.aigc = Aigc()

    @staticmethod
    def load_allergy_data(data) -> Dict[str, str]:
        return {student.name: student.allergies for student in data}

    def is_allergic(self, allergy: str, dish_name: str, ingredient: str) -> bool:
        question = f"Does having an allergy to {allergy} mean you might be allergic to {dish_name} with ingredients: {ingredient}? reply in only yes/no"
        print(question)
        response = self.aigc.create_completion(question)
        print(response)
        return "yes" in response.lower()

    def find_students_allergic_to_dish(
        self, dish_name: str, dish_ingredients: str, allergy_data: Dict[str, str]
    ) -> List[str]:
        allergic_students = []
        for student, allergies in allergy_data.items():
            if self.is_allergic(allergies, dish_name, dish_ingredients):
                allergic_students.append(student)
        return allergic_students


# Example Usage
# Set your API key in the environment variable 'OPENAI_API_KEY'
# allergy_ai = AlergyAI()
# allergy_data = allergy_ai.load_allergy_data([...]) # Load your allergy data here
# allergic_students = allergy_ai.find_students_allergic_to_dish('Pancakes', ['Eggs', 'Milk'], allergy_data)
# print(allergic_students)
