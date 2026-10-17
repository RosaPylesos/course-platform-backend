from uuid import UUID

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, require_roles

from app.models.course import Course
from app.models.user import User
from app.models.enums import UserRole

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
    statement = select(Course).where(
        Course.id == course_id
    )
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
    current_user: Annotated[
        User,
        Depends(require_roles(
            UserRole.AUTHOR, 
            UserRole.ADMIN
        )),
    ],
    db: Session = Depends(get_db),

):
    course = Course(
        **course_data.model_dump(),
        author_id = current_user.id
    )

    db.add(course)
    db.commit()
    db.refresh(course)

    return course

@router.patch("/{course_id}", response_model=CourseResponse)
def update_course(
    course_id: UUID,
    course_data: CourseUpdate,
    current_user: Annotated[
        User,
        Depends(
            require_roles(
                UserRole.AUTHOR,
                UserRole.ADMIN,
            )
        )
    ],
    db: Session = Depends(get_db),
):
    course = db.get(Course, course_id)

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    if (
        current_user.role != UserRole.ADMIN
        and course.author_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="You can only edit your own courses",
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
    current_user: Annotated[
        User,
        Depends(
            require_roles(
                UserRole.AUTHOR,
                UserRole.ADMIN,
        )),
    ],
    db: Session = Depends(get_db),
):
    course = db.get(Course, course_id)

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    if (
        current_user.role != UserRole.ADMIN
        and course.author_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own courses"
        )

    db.delete(course)
    db.commit()

    return None