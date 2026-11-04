from uuid import UUID

from app.application.exceptions import (
    AccessDeniedError,
    ResourceNotFoundError,
    InvalidInputError,
)
from app.application.unit_of_work import UnitOfWork

from app.models.course import Course
from app.models.enums import UserRole
from app.models.user import User

from app.schemas.course import CourseUpdate



class UpdateCourseCommand:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def execute(
        self,
        course_id: UUID,
        course_data: CourseUpdate,
        current_user: User,
    ) -> Course:

        course = self.uow.courses.get_by_id(course_id)

        if course is None:
            raise ResourceNotFoundError("Course not found")

        if (
            current_user.role != UserRole.ADMIN
            and course.author_id != current_user.id
        ):
            raise AccessDeniedError("You can only edit your own courses")

        update_data = course_data.model_dump(exclude_unset=True)

        if not update_data:
            raise InvalidInputError("No fields to update")

        for field in ("topic_id", "name", "difficulty"):
            if (
                field in update_data 
                and update_data[field] is None
            ):
                raise InvalidInputError(
                    f"{field} cannot be null"
                )

        if "topic_id" in update_data:
            topic = self.uow.topics.get_by_id(
                update_data["topic_id"]
            )
            if topic is None:
                raise ResourceNotFoundError("Topic not found")
        
        try:
            for field, value in update_data.items():
                setattr(course, field, value)
    
            self.uow.commit()
            self.uow.refresh(course)
        except Exception:
            self.uow.rollback()
            raise
        
        return course