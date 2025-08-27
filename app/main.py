from fastapi import FastAPI, Depends
from app.routes.auth_routes import router as auth_router
from app.routes import students, teachers, enrollments
from app.deps import require_roles
from app.models import RoleEnum
from app.database import Base, engine
Base.metadata.create_all(bind=engine)
app = FastAPI(title="Backend Test API")

app.include_router(auth_router)
app.include_router(students.router)
app.include_router(teachers.router)
app.include_router(enrollments.router)

@app.get("/admin-only")
def admin_only(_=Depends(require_roles(RoleEnum.admin))):
    return {"ok": True, "message": "Admins can see this."}

@app.get("/me-teacher")
def teacher_only(_=Depends(require_roles(RoleEnum.teacher))):
    return {"ok": True, "message": "Teachers can see this."}

@app.get("/me-student")
def student_only(_=Depends(require_roles(RoleEnum.student))):
    return {"ok": True, "message": "Students can see this."}
