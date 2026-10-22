from uuid import UUID

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, require_roles, get_current_user

from app.models.course import Course
from app.models.lesson import Lesson
from app.models.user import User
from app.models.enrollment import Enrollment
from app.models.lesson_progress import LessonProgress
from app.models.enums import (
    UserRole, 
    CourseStatus, 
    EnrollmentStatus
)

from app.schemas.lesson import LessonCreate, LessonResponse, LessonUpdate
from app.schemas.lesson_progress import LessonProgressResponse

router = APIRouter(
    prefix="/courses/{course_id}/lessons", 
    tags=["Lessons"]
)



@router.get(
    "/",
    response_model=list[LessonResponse],
    status_code=status.HTTP_200_OK,
)
def get_lessons(
    course_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> list[Lesson]:
    
    course = db.get(Course, course_id)

    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )

    if current_user.role == UserRole.ADMIN:
        pass

    elif (
        current_user.role == UserRole.AUTHOR
        and course.author_id == current_user.id
    ):
        pass

    else:
        if course.status != CourseStatus.PUBLISHED:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This course is not available",
            )

        enrollment = db.scalar(
            select(Enrollment).where(
                Enrollment.user_id == current_user.id,
                Enrollment.course_id == course_id,
                Enrollment.status == EnrollmentStatus.ACTIVE,
            )
        )

        if enrollment is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You must be actively enrolled in this course",
            )

    statement = (
        select(Lesson)
        .where(Lesson.course_id == course_id)
        .order_by(Lesson.position)
    )

    lessons = db.scalars(statement).all()

    return lessons



@router.get(
    "/{lesson_id}", 
    response_model=LessonResponse,
    status_code=status.HTTP_200_OK,
)
def get_lesson(
    course_id: UUID,
    lesson_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> Lesson:
    
    course = db.get(Course, course_id)

    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )

    if current_user.role == UserRole.ADMIN:
        pass

    elif (
        current_user.role == UserRole.AUTHOR
        and course.author_id == current_user.id
    ):
        pass

    else:
        if course.status != CourseStatus.PUBLISHED:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This course is not available",
            )

        enrollment = db.scalar(
            select(Enrollment).where(
                Enrollment.user_id == current_user.id,
                Enrollment.course_id == course_id,
                Enrollment.status == EnrollmentStatus.ACTIVE,
            )
        )

        if enrollment is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You must be actively enrolled in this course",
            )

    lesson = db.scalar(
        select(Lesson).where(
            Lesson.id == lesson_id,
            Lesson.course_id == course_id,
        )
    )

    if lesson is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found",
        )

    return lesson

@router.post(
    "/{lesson_id}/start",
    response_model=LessonProgressResponse,
    status_code=status.HTTP_200_OK,
)
def start_lesson(
    course_id: UUID,
    lesson_id: UUID,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    db: Annotated[Session, Depends(get_db)],
) -> LessonProgressResponse:

    course = db.get(Course, course_id)

    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    lesson = db.scalar(
        select(Lesson)
        .where(
            Lesson.id == lesson_id,
            Lesson.course_id == course_id,
        )
    )

    if lesson is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )

    if course.status != CourseStatus.PUBLISHED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This course is not available",
        )

    enrollment = db.scalar(
        select(Enrollment)
        .where(
            Enrollment.user_id == current_user.id,
            Enrollment.course_id == course_id,
            Enrollment.status == EnrollmentStatus.ACTIVE,
        )
    )

    if enrollment is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must be actively enrolled in this course",
        )

    progress = db.scalar(
        select(LessonProgress)
        .where(
            LessonProgress.enrollment_id == enrollment.id,
            LessonProgress.lesson_id == lesson_id,
        )
    )

    if progress is not None:
        return progress

    progress = LessonProgress(
        enrollment_id=enrollment.id,
        lesson_id=lesson_id,
        is_completed=False,
    )

    db.add(progress)
    db.commit()
    db.refresh(progress)

    return progress

@router.patch(
    "/{lesson_id}/complete",
    response_model=LessonProgressResponse,
    status_code=status.HTTP_200_OK,
)
def complete_lesson(
    course_id: UUID,
    lesson_id: UUID,
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    db: Annotated[Session, Depends(get_db)],
) -> LessonProgressResponse:

    course = db.get(Course, course_id)

    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )

    lesson = db.scalar(
        select(Lesson)
        .where(
            Lesson.id == lesson_id,
            Lesson.course_id == course_id,
        )
    )

    if lesson is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found",
        )

    if course.status != CourseStatus.PUBLISHED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This course is not available",
        )

    enrollment = db.scalar(
        select(Enrollment)
        .where(
            Enrollment.user_id == current_user.id,
            Enrollment.course_id == course_id,
            Enrollment.status == EnrollmentStatus.ACTIVE,
        )
    )

    if enrollment is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must be actively enrolled in this course",
        )

    progress = db.scalar(
        select(LessonProgress)
        .where(
            LessonProgress.enrollment_id == enrollment.id,
            LessonProgress.lesson_id == lesson_id,
        )
    )

    if progress is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You must start the lesson before completing it",
        )

    if not progress.is_completed:
        progress.is_completed = True

    db.flush()

    lessons_total = db.scalar(
        select(func.count(Lesson.id))
        .where(Lesson.course_id == course_id)
    )

    lessons_completed = db.scalar(
        select(func.count(LessonProgress.id))
        .where(
            LessonProgress.enrollment_id == enrollment.id,
            LessonProgress.is_completed.is_(True),
        )
    )

    if(
        lessons_total > 0
        and lessons_completed == lessons_total
    ):
        enrollment.status = EnrollmentStatus.COMPLETED

    db.commit()
    db.refresh(progress)

    return progress



@router.post(
    "/", 
    response_model=LessonResponse, 
    status_code=status.HTTP_201_CREATED,
)
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
    db: Annotated[Session, Depends(get_db)],
) -> Lesson:
    
    course = db.get(Course, course_id)

    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )

    if (
        current_user.role != UserRole.ADMIN
        and course.author_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
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



@router.patch(
    "/{lesson_id}", 
    response_model=LessonResponse,
    status_code=status.HTTP_200_OK,
)
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
    db: Annotated[Session, Depends(get_db)],
) -> Lesson:
    
    course = db.get(Course, course_id)

    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )

    if (
        current_user.role != UserRole.ADMIN
        and course.author_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
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
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found",
        )

    update_data = lesson_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(lesson, field, value)

    db.commit()
    db.refresh(lesson)

    return lesson



@router.delete(
    "/{lesson_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
)
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
    db: Annotated[Session, Depends(get_db)],
) -> None:

    course = db.get(Course, course_id)

    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )

    if (
        current_user.role != UserRole.ADMIN
        and course.author_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
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
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found",
        )

    db.delete(lesson)
    db.commit()