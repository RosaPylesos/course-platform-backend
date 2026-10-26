from uuid import UUID

from app.application.exceptions import (
    AccessDeniedError,
    ConflictError,
    ResourceNotFoundError,
)
from app.application.unit_of_work import UnitOfWork

from app.models.course_tag import CourseTag
from app.models.enums import UserRole
from app.models.user import User



class AssignTagToCourseCommand:
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

        tag = self.uow.tags.get_by_id(tag_id)

        if tag is None:
            raise ResourceNotFoundError("Tag not found")

        if (
            current_user.role != UserRole.ADMIN
            and course.author_id != current_user.id
        ):
            raise AccessDeniedError(
                "You cannt manage tags for this course"
            )

        existing = self.uow.course_tags.get_by_ids(
            course_id,
            tag_id,
        )

        if existing is not None:
            raise ConflictError(
                "This tag is already assigned to the course"
            )

        try:
            course_tag = CourseTag(
                course_id=course_id,
                tag_id=tag_id,
            )
            self.uow.course_tags.add(course_tag)
            self.uow.commit()
        except Exception:
            self.uow.rollback()
            raise