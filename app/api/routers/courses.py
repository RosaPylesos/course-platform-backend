from uuid import UUID

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_db, 
    require_roles, 
    get_current_user
)

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

from app.schemas.course import (
    CourseResponse, 
    CourseCreate, 
    CourseUpdate
)
from app.schemas.lesson_progress import (
    CourseProgressResponse, 
    LessonProgressItem
)

router = APIRouter(
    prefix="/courses", 
    tags=["Courses"]
)

@router.get(
    "/", 
    response_model=list[CourseResponse],
    status_code=status.HTTP_200_OK,
)
def get_courses(
    db: Annotated[Session, Depends(get_db)],
) -> list[Course]:
    
    courses = db.scalars(
        select(Course).where(
            Course.status == CourseStatus.PUBLISHED
        )
    ).all()

    return courses



@router.get(
    "/{course_id}", 
    response_model=CourseResponse,
    status_code=status.HTTP_200_OK,
)
def get_course(
    course_id: UUID,
    db: Annotated[Session, Depends(get_db)],
) -> Course:
    
    statement = select(Course).where(
        Course.id == course_id
    )
    course = db.scalar(statement)

    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )

    if course.status != CourseStatus.PUBLISHED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This course is not published yet"
        )

    return course



@router.get(
    "/{course_id}/progress",
    response_model=CourseProgressResponse,
    status_code=status.HTTP_200_OK,
)
def get_course_progress(
    course_id: UUID,
    current_user: Annotated[
        User, 
        Depends(get_current_user)
    ],
    db: Annotated[Session, Depends(get_db)],
) -> CourseProgressResponse:

    course = db.get(Course, course_id)

    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )

    enrollment = db.scalar(
        select(Enrollment)
        .where(
            Enrollment.course_id == course_id,
            Enrollment.user_id == current_user.id,
            Enrollment.status.in_([
                EnrollmentStatus.ACTIVE,
                EnrollmentStatus.COMPLETED,
            ]),
        )
    )

    if enrollment is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You must be actively enrolled on this course",
        )

    lessons = db.scalars(
        select(Lesson)
        .where(
            Lesson.course_id == course_id
        )
        .order_by(Lesson.position)
    ).all()

    progress_records = db.scalars(
        select(LessonProgress)
        .where(
            LessonProgress.enrollment_id == enrollment.id
        )
    ).all()

    progress_by_lesson_id = {
        progress.lesson_id: progress
        for progress in progress_records
    }

    lesson_items = [
        LessonProgressItem(
            lesson_id=lesson.id,
            lesson_name=lesson.name,
            is_started=lesson.id in progress_by_lesson_id,
            is_completed=(
                progress_by_lesson_id[lesson.id].is_completed
                if lesson.id in progress_by_lesson_id
                else False
            ),
        )
        for lesson in lessons
    ]

    lessons_started = len(progress_records)
    lessons_completed = sum(
        progress.is_completed
        for progress  in progress_records
    )

    return CourseProgressResponse(
        course_id=course.id,
        lessons_total=len(lessons),
        lessons_started=lessons_started,
        lessons_completed=lessons_completed,
        lessons=lesson_items
    )



@router.post(
    "/", 
    response_model=CourseResponse, 
    status_code=status.HTTP_201_CREATED,
)
def create_course(
    course_data: CourseCreate,
    current_user: Annotated[
        User,
        Depends(require_roles(
            UserRole.AUTHOR, 
            UserRole.ADMIN
        )),
    ],
    db: Annotated[Session, Depends(get_db)],

) -> Course:
    
    course = Course(
        **course_data.model_dump(),
        author_id = current_user.id
    )

    db.add(course)
    db.commit()
    db.refresh(course)

    return course



@router.patch(
    "/{course_id}", 
    response_model=CourseResponse,
    status_code=status.HTTP_200_OK,
)
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
    db: Annotated[Session, Depends(get_db)],
) -> Course:
    
    course = db.get(Course, course_id)

    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    if (
        current_user.role != UserRole.ADMIN
        and course.author_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
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
    db: Annotated[Session, Depends(get_db)],
) -> None:
    
    course = db.get(Course, course_id)

    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    if (
        current_user.role != UserRole.ADMIN
        and course.author_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own courses"
        )

    db.delete(course)
    db.commit()

    return None