from uuid import UUID

from app.application.exceptions import (
    AccessDeniedError,
    ResourceNotFoundError,
)
from app.application.unit_of_work import UnitOfWork

from app.models.enums import UserRole
from app.models.user import User



class UnassignTagFromCourseCommand:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def execute(
        self,
        course_id: UUID,
        tag_id: UUID,
        current_user: User,
    ) -> None:

        course = self.uow.courses.get_by_id(course_id)

        if course is None:
            raise ResourceNotFoundError("Course not found")

        if (
            current_user.role != UserRole.ADMIN
            and course.author_id != current_user.id
        ):
            raise AccessDeniedError(
                "You cannot manage tags for this course"
            )

        course_tag = self.uow.course_tags.get_by_ids(
            course_id,
            tag_id,
        )

        if course_tag is None:
            raise ResourceNotFoundError(
                "This tag is not assigned to the course"
            )

        try:
            self.uow.course_tags.delete(course_tag)
            self.uow.commit()
        except Exception:
            self.uow.rollback()
            raise