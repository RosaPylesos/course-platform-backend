from uuid import UUID

from app.application.exceptions import(
    AccessDeniedError,
    ResourceNotFoundError,
)
from app.application.unit_of_work import UnitOfWork

from app.models.enums import UserRole
from app.models.user import User



class DeleteLessonCommand:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def execute(
        self,
        course_id: UUID,
        lesson_id: UUID,
        user: User,
    ) -> None:
        course = self.uow.courses.get_by_id(course_id)

        if course is None:
            raise ResourceNotFoundError("Course not found")

        if (
            user.role != UserRole.ADMIN
            and course.author_id != user.id
        ):
            raise AccessDeniedError(
                "You can only delete lessons from your own courses"
            )

        lesson = self.uow.lessons.get_by_id_for_course(
            lesson_id=lesson_id,
            course_id=course_id,
        )

        if lesson is None:
            raise ResourceNotFoundError("Lesson not found")

        try:
            self.uow.lessons.delete(lesson)
            self.uow.commit()
        except Exception:
            self.uow.rollback()
            raise