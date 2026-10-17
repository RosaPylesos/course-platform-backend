from uuid import UUID

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, require_roles, get_current_user

from app.models.course import Course
from app.models.lesson import Lesson
from app.models.user import User
from app.models.enums import UserRole, CourseStatus

from app.schemas.lesson import LessonCreate, LessonResponse, LessonUpdate

router = APIRouter(
    prefix="/courses/{course_id}/lessons", 
    tags=["Lessons"]
)

@router.get("/",response_model=list[LessonResponse])
def get_lessons(
    course_id: UUID,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    db: Session = Depends(get_db)
):
    course = db.get(Course, course_id)

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    if (
        current_user.role == UserRole.STUDENT
        and course.status == CourseStatus.DRAFT
    ):
        raise HTTPException(
            status_code=403,
            detail="This course is not published yet",
        )

    if (
        current_user.role == UserRole.AUTHOR
        and course.author_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="You can only view lessons in your own courses"
        )

    statement = (
        select(Lesson)
        .where(Lesson.course_id == course_id)
        .order_by(Lesson.position)
    )

    lessons = db.scalars(statement).all()

    return lessons

@router.get("/{lesson_id}", response_model=LessonResponse)
def get_lesson(
    course_id: UUID,
    lesson_id: UUID,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    db: Session = Depends(get_db)
):
    course = db.get(Course, course_id)

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    if (
        current_user.role == UserRole.STUDENT
        and course.status == CourseStatus.DRAFT
    ):
        raise HTTPException(
            status_code=403,
            detail="This course is not published yet",
        )

    if (
        current_user.role == UserRole.AUTHOR
        and course.author_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="You can only view lessons in your own courses",
        )

    lesson = db.scalar(
        select(Lesson).where(
            Lesson.id == lesson_id,
            Lesson.course_id == course_id,
        )
    )

    if lesson is None:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found",
        )

    return lesson


@router.post("/", response_model=LessonResponse, status_code=201)
def create_lesson(
    course_id: UUID,
    lesson_data: LessonCreate,
    current_user: Annotated[
        User,
        Depends(
            require_roles(
                UserRole.AUTHOR,
                UserRole.ADMIN,
            )
        ),
    ],
    db: Session = Depends(get_db)
):
    course = db.get(Course, course_id)

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    if (
        current_user.role != UserRole.ADMIN
        and course.author_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="You can only add lessons to your own courses"
        )

    statement = select(func.max(Lesson.position)).where(
        Lesson.course_id == course_id
    )
    max_position = db.scalar(statement)
    next_position = (max_position or 0) + 1

    lesson = Lesson(
        **lesson_data.model_dump(),
        course_id=course_id,
        position=next_position,
    )

    db.add(lesson)
    db.commit()
    db.refresh(lesson)

    return lesson

@router.patch("/{lesson_id}", response_model=LessonResponse)
def update_lesson(
    course_id: UUID,
    lesson_id: UUID,
    lesson_data: LessonUpdate,
    current_user: Annotated[
        User,
        Depends(
            require_roles(
                UserRole.AUTHOR,
                UserRole.ADMIN,
            )
        ),
    ],
    db: Session = Depends(get_db),
):
    course = db.get(Course, course_id)

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    if (
        current_user.role != UserRole.ADMIN
        and course.author_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="You can only edit lessons in your own courses"
        )

    lesson = db.scalar(
        select(Lesson).where(
            Lesson.id == lesson_id,
            Lesson.course_id == course_id,
        )
    )

    if lesson is None:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found",
        )

    update_data = lesson_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(lesson, field, value)

    db.commit()
    db.refresh(lesson)

    return lesson

@router.delete("/{lesson_id}", status_code=204)
def delete_lesson(
    course_id: UUID,
    lesson_id: UUID,
    current_user: Annotated[
        User,
        Depends(
            require_roles(
                UserRole.AUTHOR,
                UserRole.ADMIN,
            )
        ),
    ],
    db: Session = Depends(get_db),
):

    course = db.get(Course, course_id)

    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found",
        )

    if (
        current_user.role != UserRole.ADMIN
        and course.author_id != current_user.id
    ):
        raise HTTPException(
            status_code=403,
            detail="You can only delete lessons from your own courses",
        )

    lesson = db.scalar(
        select(Lesson).where(
            Lesson.id == lesson_id,
            Lesson.course_id == course_id,
        )
    )

    if lesson is None:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found",
        )

    db.delete(lesson)
    db.commit()