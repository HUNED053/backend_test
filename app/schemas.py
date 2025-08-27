from pydantic import BaseModel, EmailStr
from typing import Literal
from datetime import datetime
from typing import List
from pydantic import BaseModel, EmailStr

RoleLiteral = Literal["admin", "student", "teacher"]

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str
    role: RoleLiteral

class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    role: RoleLiteral
    class Config:
        from_attributes = True

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class StudentBase(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None
    course: str | None = None

class StudentCreate(StudentBase):
    pass

class StudentOut(StudentBase):
    id: int
    class Config:
        from_attributes = True


class TeacherBase(BaseModel):
    name: str
    department: str

class TeacherCreate(TeacherBase):
    pass

class TeacherOut(TeacherBase):
    id: int
    class Config:
        from_attributes = True


class EnrollmentBase(BaseModel):
    student_id: int
    teacher_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentOut(BaseModel):
    student_id: int
    teacher_id: int
    enrolled_on: datetime
    class Config:
        from_attributes = True