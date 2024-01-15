# init_db.py

from flask import Flask
from app import db, Student
import json

app = Flask(__name__)

# Configure the Flask app and SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@localhost/foodcourt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def load_fake_students():
    with open('fake_data.json', 'r') as json_file:
        fake_students = json.load(json_file)
        return fake_students


# Initialize the SQLAlchemy database
db.init_app(app)

# Create the database tables
with app.app_context():
    db.create_all()

    # Insert fake data into the "student" table if it doesn't exist
    if not Student.query.first():
        fake_students_data = load_fake_students()
        for fake_student_data in fake_students_data:
            student = Student(name=fake_student_data['name'], allergies=fake_student_data['allergies'])
            db.session.add(student)
        db.session.commit()

print("Database initialized and seeded.")
