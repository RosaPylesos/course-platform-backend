from uuid import UUID

from app.application.exceptions import (
    AccessDeniedError,
    ResourceNotFoundError,
)
from app.application.unit_of_work import UnitOfWork

from app.models.enums import UserRole
from app.models.user import User



class DeleteCourseCommand:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def execute(
        self,
        course_id: UUID,
        current_user: User,
    ) -> None:

        course = self.uow.courses.get_by_id(course_id)

        if course is None:
            raise ResourceNotFoundError("Course not found")

        if (
            current_user.role != UserRole.ADMIN
            and course.author_id != current_user.id
        ):
            raise AccessDeniedError("You can only delete your own courses")

        self.uow.courses.delete(course)
        self.uow.commit()