from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from flask import current_app, g

db = SQLAlchemy(current_app)


class Student(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    allergies = Column(String(500))  # Store allergies as a JSON string

    def __init__(self, name, allergies):
        self.name = name
        self.allergies = allergies