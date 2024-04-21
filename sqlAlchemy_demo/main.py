from init_db import engine
from sqlAlchemy_demo.models import Student, Class, students_classes_association
from sqlalchemy.orm import sessionmaker
from sqlalchemy import not_, func
from datetime import time


Session = sessionmaker(bind=engine)
session = Session()


def base_select():
    students = session.query(Student).order_by(Student.name).all()
    classes = session.query(Class).order_by(Class.time).all()

    for t in students:
        print(f"ID: {t.id} name: {t.name} ")
    for c in classes:
        print(f"TIME: {c.time} subject: {c.name} ")


def updating_data():
    kows = session.query(Student).filter(Student.name.like("Kow%")).all()
    print(kows)
    others = session.query(Student).filter(Student.name.not_like("Kow%")).all()
    print(others)

    afternoon_classes = session.query(Class).filter(Class.time >= time(12)).all()
    before_10am_classes = session.query(Class).filter(Class.time <= time(10)).all()

    for s in kows:
        s.classes.extend(afternoon_classes)
    for s in others:
        s.classes.extend(before_10am_classes)

    session.commit()

    print(session.query(Student).filter(Student.name.like("Kow%")).all())
    print(session.query(Student).filter(not_(Student.name.like("Kow%"))).all())


def grouping():
    students_in_classes = (
        session.query(Class.name, func.count(Student.id))
                      .join(Class.students, isouter=True)
                      .group_by(Class.name)
                      .all()
    )

    print(students_in_classes)


def print_classes():
    #lazy loading overhere
    for c in session.query(Class).all():
        print(f"Class: {c.name} | Students: {', '.join([s.name for s in c.students])}")


#updating_data()
engine.echo = False
grouping()
#print_classes()
