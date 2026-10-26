from uuid import UUID

from app.application.exceptions import (
    AccessDeniedError,
    BusinessRuleError,
    ConflictError,
    ResourceNotFoundError,
)
from app.application.unit_of_work import UnitOfWork

from app.models.course import Course
from app.models.enums import CourseStatus, UserRole
from app.models.user import User



class PublishCourseCommand:
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
                "You can only publish your own courses"
            )

        if course.status != CourseStatus.DRAFT:
            raise ConflictError(
                "Only draft courses can be published"
            )

        lessons_total = self.uow.lessons.count_by_course(course_id)

        if lessons_total == 0:
            raise BusinessRuleError(
                "A course must have at least one lesson before publishing"
            )

        try:
            course.status = CourseStatus.PUBLISHED
            self.uow.commit()
        except Exception:
            self.uow.rollback()
            raise

        self.uow.refresh(course)

        return course