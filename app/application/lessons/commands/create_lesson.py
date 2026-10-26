from uuid import UUID

from app.application.exceptions import(
    AccessDeniedError,
    ResourceNotFoundError
)
from app.application.unit_of_work import UnitOfWork

from app.models.enums import (
    UserRole,
    CourseStatus,
    EnrollmentStatus,
)
from app.models.lesson import Lesson
from app.models.user import User

from app.schemas.lesson import LessonCreate



class CreateLessonCommand:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def execute(
        self,
        course_id: UUID,
        lesson_data: LessonCreate,
        user: User,
    ) -> Lesson:
        
        course = self.uow.courses.get_by_id(course_id)

        if course is None:
            raise ResourceNotFoundError("Course not found")

        is_published = course.status == CourseStatus.PUBLISHED

        if(
            user.role != UserRole.ADMIN
            and course.author_id != user.id
        ):
            raise AccessDeniedError(
                "You can only add lessons to your own courses"
            )

        max_position = self.uow.lessons.get_max_position_by_course(
            course_id
        )
        next_position = (max_position or 0) + 1

        lesson = Lesson(
            **lesson_data.model_dump(),
            course_id=course_id,
            position=next_position,
        )

        try:
            self.uow.lessons.add(lesson)

            if is_published:
                enrollments = self.uow.enrollments.list_by_course(course_id)

                for enrollment in enrollments:
                    if enrollment.status == EnrollmentStatus.COMPLETED:
                        enrollment.status = EnrollmentStatus.ACTIVE

            self.uow.commit()
            self.uow.refresh(lesson)
        except Exception:
            self.uow.rollback()
            raise

        return lesson