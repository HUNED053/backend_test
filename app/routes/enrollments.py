from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app import schemas, models
from app.database import get_db

router = APIRouter(prefix="/enrollments", tags=["enrollments"])


def fake_send_email(student_email: str, teacher_name: str):
    print(f"[EMAIL] Sent enrollment confirmation to {student_email} for teacher {teacher_name}")


@router.post("/", response_model=schemas.EnrollmentOut, status_code=201)
def assign_student(
    data: schemas.EnrollmentCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    student = db.query(models.Student).filter(models.Student.id == data.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    teacher = db.query(models.Teacher).filter(models.Teacher.id == data.teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    existing = (
        db.query(models.Enrollment)
        .filter_by(student_id=data.student_id, teacher_id=data.teacher_id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Already enrolled")

    enrollment = models.Enrollment(
        student_id=data.student_id,
        teacher_id=data.teacher_id,
        enrolled_on=datetime.utcnow()
    )
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)

    background_tasks.add_task(fake_send_email, student.email, teacher.name)

    return enrollment


@router.get("/teacher/{teacher_id}", response_model=List[schemas.StudentOut])
def get_students_of_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")

    students = [enrollment.student for enrollment in teacher.students]
    return students


@router.get("/student/{student_id}", response_model=List[schemas.TeacherOut])
def get_teachers_of_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    teachers = [enrollment.teacher for enrollment in student.teachers]
    return teachers
