from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models
from app.database import get_db
from app.redis_cache import get_cache, set_cache, delete_cache

router = APIRouter(prefix="/students", tags=["students"])


@router.post("/", response_model=schemas.StudentOut, status_code=201)
def create_student(data: schemas.StudentCreate, db: Session = Depends(get_db)):
    if db.query(models.Student).filter(models.Student.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    student = models.Student(**data.dict())
    db.add(student)
    db.commit()
    db.refresh(student)


    delete_cache("students:list")
    return student


@router.get("/", response_model=List[schemas.StudentOut])
def list_students(db: Session = Depends(get_db)):
    cache_key = "students:list"
    cached = get_cache(cache_key)
    if cached:
        return cached

    students = db.query(models.Student).all()
    result = [schemas.StudentOut.model_validate(student).dict() for student in students]


    set_cache(cache_key, result, expire_seconds=30)
    return result


@router.get("/{student_id}", response_model=schemas.StudentOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@router.put("/{student_id}", response_model=schemas.StudentOut)
def update_student(student_id: int, data: schemas.StudentCreate, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    for key, value in data.dict().items():
        setattr(student, key, value)
    db.commit()
    db.refresh(student)


    delete_cache("students:list")
    return student


@router.delete("/{student_id}", status_code=204)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()


    delete_cache("students:list")
    return None
