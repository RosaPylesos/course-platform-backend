from uuid import UUID

from app.application.exceptions import (
    AccessDeniedError,
    ConflictError,
    ResourceNotFoundError,
)
from app.application.unit_of_work import UnitOfWork

from app.models.course import Course
from app.models.enums import CourseStatus, UserRole
from app.models.user import User



class ArchiveCourseCommand:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def execute(
        self,
        course_id: UUID,
        current_user: User,
    ) -> Course:

        course = self.uow.courses.get_by_id(course_id)

        if course is None:
            raise ResourceNotFoundError("Course not found")

        if (
            current_user.role != UserRole.ADMIN
            and course.author_id != current_user.id
        ):
            raise AccessDeniedError(
                "You can only archive your own courses"
            )

        if course.status != CourseStatus.PUBLISHED:
            raise ConflictError(
                "Only published courses can be archived"
            )

        try:
            course.status = CourseStatus.ARCHIVED
            self.uow.commit()
            self.uow.refresh(course)
        except Exception:
            self.uow.rollback()
            raise

        return course