from uuid import UUID

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db

from app.models.course import Course
from app.models.lesson import Lesson
from app.models.enrollment import Enrollment
from app.models.user import User
from app.models.enums import EnrollmentStatus, CourseStatus
from app.models.lesson_progress import LessonProgress

from app.schemas.enrollment import EntrollmentCreate, EnrollmentResponse

router = APIRouter(
    prefix="/enrollments",
    tags=["Enrollments"],
)

@router.get(
    "/",
    response_model=list[EnrollmentResponse],
    status_code=status.HTTP_200_OK,
)
def get_my_enrollments(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> list[Enrollment]:
    enrollments = db.scalars(
        select(Enrollment).where(
            Enrollment.user_id == current_user.id
        )
    ).all()

    return list(enrollments)

@router.post(
    "/",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_enrollment(
    enrollment_data: EntrollmentCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Enrollment:
    course = db.scalar(
        select(Course).where(
            Course.id == enrollment_data.course_id
        )
    )

    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )

    if course.status != CourseStatus.PUBLISHED:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Enrollment is only available for published courses",
        )

    existing_enrollment = db.scalar(
        select(Enrollment).where(
            Enrollment.user_id == current_user.id,
            Enrollment.course_id == enrollment_data.course_id,
        )
    )

    if existing_enrollment is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You are already enrolled in this course",
        )

    enrollment = Enrollment(
        user_id=current_user.id,
        course_id=enrollment_data.course_id,
        status=EnrollmentStatus.ACTIVE,
    )

    db.add(enrollment)

    try:
        db.commit()
        db.refresh(enrollment)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You are already enrolled in this course",
        )

    return enrollment

@router.patch(
    "/{enrollment_id}/cancel",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_200_OK,
)
def cancel_enrollment(
    enrollment_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Enrollment:
    enrollment = db.scalar(
        select(Enrollment).where(
            Enrollment.id == enrollment_id,
            Enrollment.user_id == current_user.id,
        )
    )

    if enrollment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found",
        )

    if enrollment.status != EnrollmentStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Only active enrollments can be cancelled"
        )

    enrollment.status = EnrollmentStatus.CANCELLED

    db.commit()
    db.refresh(enrollment)

    return enrollment

@router.patch(
    "/{enrollment_id}/restore",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_200_OK,
)
def restore_enrollment(
    enrollment_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Enrollment:
    enrollment = db.scalar(
        select(Enrollment).where(
            Enrollment.id == enrollment_id,
            Enrollment.user_id == current_user.id,
        )
    )

    if enrollment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found",
        )

    if enrollment.status != EnrollmentStatus.CANCELLED:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Only cancelled enrollments can be restored",
        )

    enrollment.status = EnrollmentStatus.ACTIVE

    course = db.get(Course, enrollment.course_id)

    if course is not None and course.status == CourseStatus.PUBLISHED:
        lessons_total = db.scalar(
            select(
                func.count(Lesson.id)
            )
            .where(Lesson.course_id == enrollment.course_id)
        )
        
        lessons_completed = db.scalar(
            select(
                func.count(LessonProgress.id)
            )
            .where(
                LessonProgress.enrollment_id == enrollment.id,
                LessonProgress.is_completed.is_(True)
            )
        )

        if (
            lessons_total > 0
            and lessons_completed == lessons_total
        ):
            enrollment.status == EnrollmentStatus.COMPLETED

    db.commit()
    db.refresh(enrollment)

    return enrollment