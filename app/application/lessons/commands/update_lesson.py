from uuid import UUID

from app.application.exceptions import(
    AccessDeniedError,
    ResourceNotFoundError,
    InvalidInputError,
)
from app.application.unit_of_work import UnitOfWork

from app.models.enums import UserRole
from app.models.lesson import Lesson
from app.models.user import User

from app.schemas.lesson import LessonUpdate



class UpdateLessonCommand:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def execute(
        self,
        course_id: UUID,
        lesson_id: UUID,
        lesson_data: LessonUpdate,
        user: User,
    ) -> Lesson:
        course = self.uow.courses.get_by_id(course_id)

        if course is None:
            raise ResourceNotFoundError("Course not found")

        if(
            user.role != UserRole.ADMIN
            and course.author_id != user.id
        ):
            raise AccessDeniedError(
                "You can only edit lessons in your own courses"
            )

        lesson = self.uow.lessons.get_by_id_for_course(
            lesson_id=lesson_id,
            course_id=course_id,
        )

        if lesson is None:
            raise ResourceNotFoundError("Lesson not found")

        update_data = lesson_data.model_dump(
            exclude_unset=True,
            mode="json"
        )

        if not update_data:
            raise InvalidInputError("No fields to update")

        if (
            "name" in update_data 
            and update_data["name"] is None
        ):
            raise InvalidInputError("Lesson name cannot be null")

        if (
            "content" in update_data
            and update_data["content"] is None
        ):
            raise InvalidInputError("Lesson content cannot be null")

        try:
            for field, value in update_data.items():
                setattr(lesson, field, value)

            self.uow.commit()
            self.uow.refresh(lesson)
        except Exception:
            self.uow.rollback()
            raise

        return lesson