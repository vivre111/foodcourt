from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from aigc import AlergyAI


import os

app = Flask(__name__)

# Use the DATABASE_URL environment variable for the database connection URL.
# Provide a default connection URL with placeholders for the username, password, host, and database name.
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "mysql://root:admin@localhost/foodcourt"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Student(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    allergies = Column(String(500))  # Store allergies as a JSON string

    def __init__(self, name, allergies):
        self.name = name
        self.allergies = allergies


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/student/create", methods=["GET", "POST"])
def create_student():
    if request.method == "POST":
        name = request.form.get("name")
        allergies = request.form.get("allergies")

        # Create a new student and add it to the database
        new_student = Student(name=name, allergies=allergies)
        db.session.add(new_student)
        db.session.commit()


@app.route("/student", methods=["GET", "POST"])
def student_form():
    # Retrieve all students from the database

    if request.method == "POST":
        name = request.form.get("name")
        allergies = request.form.get("allergies")

        # Create a new student and add it to the database
        new_student = Student(name=name, allergies=allergies)
        db.session.add(new_student)
        db.session.commit()
    students = Student.query.all()
    # Create a list of dictionaries containing student IDs and allergies
    student_data = [
        {"id": student.id, "name": student.name, "allergies": student.allergies}
        for student in students
    ]

    return render_template("student.html", student_data=student_data)


@app.route("/cook", methods=["GET", "POST"])
def cook_dish():
    if request.method == "POST":
        dish_name = request.form.get("dish_name")
        ingredients = request.form.get("ingredients")

        # Here, you can save the dish name and ingredients to your database or perform any other action.
        # For example, you can create a new table to store dish information and save the data there.

        # For demonstration purposes, let's assume you have a Dish model:
        # dish = Dish(name=dish_name, ingredients=ingredients)
        # db.session.add(dish)
        # db.session.commit()
        alergyAI = AlergyAI()
        students = Student.query.all()
        student_data = [
            {"id": student.id, "name": student.name, "allergies": student.allergies}
            for student in students
        ]

        allergy_data = alergyAI.load_allergy_data(students)
        allergic_students = alergyAI.find_students_allergic_to_dish(
            dish_name, ingredients, allergy_data
        )
        filtered_students = [student for student in students if student.name in allergic_students]

        # here render the allergic_students(id,name,allergies) 
        return render_template("allergic_students.html", allergic_students=filtered_students, dish_name=dish_name)


    return render_template("cook.html")


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        uploaded_file = request.files["file"]
        if uploaded_file:
            uploaded_file.save(uploaded_file.filename)
            return "File uploaded successfully!"
    return render_template("upload.html")


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
