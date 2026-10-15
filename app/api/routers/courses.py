from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_db

from app.models.course import Course

from app.schemas.course import CourseResponse, CourseCreate, CourseUpdate

router = APIRouter(
    prefix="/courses", 
    tags=["Courses"]
)

@router.get("/", response_model=list[CourseResponse])
def get_courses(db: Session = Depends(get_db)):
    statement = select(Course)
    courses = db.scalars(statement).all()

    return courses

@router.get("/{course_id}", response_model=CourseResponse)
def get_course(
    course_id: UUID,
    db: Session = Depends(get_db)
):
    statement = select(Course).where(Course.id== course_id)
    course = db.scalar(statement)

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    return course

@router.post("/", response_model=CourseResponse, status_code=201)
def create_course(
    course_data: CourseCreate,
    db: Session = Depends(get_db),
):
    course = Course(**course_data.model_dump())

    db.add(course)
    db.commit()
    db.refresh(course)

    return course

@router.patch("/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: UUID,
    course_data: CourseUpdate,
    db: Session = Depends(get_db),
):
    course = db.get(Course, course_id)

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    update_data = course_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(course, field, value)

    db.commit()
    db.refresh(course)

    return course

@router.delete("/{course_id}", status_code=204)
def delete_course(
    course_id: UUID,
    db: Session = Depends(get_db),
):
    course = db.get(Course, course_id)

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    db.delete(course)
    db.commit()

    return None