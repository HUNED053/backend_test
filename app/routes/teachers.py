from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models
from app.database import get_db

router = APIRouter(prefix="/teachers", tags=["teachers"])

@router.post("/", response_model=schemas.TeacherOut, status_code=201)
def create_teacher(data: schemas.TeacherCreate, db: Session = Depends(get_db)):
    teacher = models.Teacher(**data.dict())
    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    return teacher

@router.get("/", response_model=List[schemas.TeacherOut])
def list_teachers(db: Session = Depends(get_db)):
    return db.query(models.Teacher).all()

@router.get("/{teacher_id}", response_model=schemas.TeacherOut)
def get_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher

@router.put("/{teacher_id}", response_model=schemas.TeacherOut)
def update_teacher(teacher_id: int, data: schemas.TeacherCreate, db: Session = Depends(get_db)):
    teacher = db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    for key, value in data.dict().items():
        setattr(teacher, key, value)
    db.commit()
    db.refresh(teacher)
    return teacher

@router.delete("/{teacher_id}", status_code=204)
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher = db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    db.delete(teacher)
    db.commit()
    return None
