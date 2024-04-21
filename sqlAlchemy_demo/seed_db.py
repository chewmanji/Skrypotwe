from sqlalchemy.orm import sessionmaker
from sqlAlchemy_demo.models import Student, Class
from init_db import engine
from datetime import time

Session = sessionmaker(bind=engine)

session = Session()

subjects = [
    "Math",
    "English",
    "History",
    "Biology",
    "Chemistry",
    "Physics",
    "Computer Science",
    "Art",
    "Music",
    "Physical Education",
]
times = [
    time(12, 0),
    time(9, 30),
    time(8, 30),
    time(10, 30),
    time(10, 0),
    time(8, 0),
    time(11, 0),
    time(9, 0),
    time(12, 30),
    time(11, 30),
]

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Create and add Class objects
for i, subject in enumerate(subjects):
    class_obj = Class(name=subject, time=times[i])
    session.add(class_obj)

teacher1 = Student(name="Kowalski")
teacher2 = Student(name="Nowak")
teacher3 = Student(name="Iksiński")
teacher4 = Student(name="Kowal")

session.add_all([teacher1, teacher2, teacher3, teacher4])

#without commit() changes won't be applied
session.commit()
