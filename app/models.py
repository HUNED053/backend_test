from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import enum

class RoleEnum(str, enum.Enum):
    admin = "admin"
    student = "student"
    teacher = "teacher"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.student)

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True)
    course = Column(String, nullable=True)

    teachers = relationship("Enrollment", back_populates="student")

class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    department = Column(String, nullable=False)

    students = relationship("Enrollment", back_populates="teacher")

class Enrollment(Base):
    __tablename__ = "enrollments"

    student_id = Column(Integer, ForeignKey("students.id"), primary_key=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), primary_key=True)
    enrolled_on = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="teachers")
    teacher = relationship("Teacher", back_populates="students")
