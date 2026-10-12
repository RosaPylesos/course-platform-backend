from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_db

from app.models.course import Course

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.get("/")
def get_courses(db: Session = Depends(get_db)):
    statement = select(Course)
    courses = db.scalars(statement).all()
    return courses