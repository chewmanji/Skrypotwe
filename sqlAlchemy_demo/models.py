from sqlalchemy import ForeignKey, String, Integer, Column, Time, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List


class Base(DeclarativeBase):
    pass


students_classes_association = Table(
    "students_classes",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("class_id", Integer, ForeignKey("classes.id"), primary_key=True),
)


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30))
    classes: Mapped[List["Class"]] = relationship(
        secondary=students_classes_association, back_populates="students"
    )

    def __repr__(self) -> str:
        return f"name = {self.name}, classes = {[(c.id, c.name) for c in self.classes]}"


class Class(Base):
    __tablename__ = "classes"
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
    time = Column(Time)
    students: Mapped[List["Student"]] = relationship(
        secondary=students_classes_association, back_populates="classes"
    )

    def __repr__(self) -> str:
        return f"name = {self.name}, time = {self.time}, students = {[(s.id, s.name) for s in self.students]}"
