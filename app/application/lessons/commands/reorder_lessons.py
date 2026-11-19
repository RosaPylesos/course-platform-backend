from uuid import UUID

from app.application.exceptions import (
    AccessDeniedError,
    InvalidInputError,
    ResourceNotFoundError,
)
from app.application.unit_of_work import UnitOfWork

from app.models.enums import UserRole
from app.models.user import User



class ReorderLessonsCommand:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def execute(
        self,
        course_id: UUID,
        lesson_ids: list[UUID],
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
                "You can only reorder lessons in your own courses"
            )

        if len(lesson_ids) != len(set(lesson_ids)):
            raise InvalidInputError(
                "Lesson IDs must be unique"
            )

        lessons = self.uow.lessons.list_by_course(course_id)

        current_ids = {lesson.id for lesson in lessons}
        requested_ids = set(lesson_ids)

        if (
            requested_ids != current_ids
            or len(lesson_ids) != len(lessons)
        ):
            raise InvalidInputError(
                "You must provide every lesson in the course exactly once"
            )

        if not lessons:
            raise InvalidInputError(
                "There are no lessons to reorder"
            )

        lessons_by_id = {
            lesson.id: lesson
            for lesson in lessons
        }

        max_position = max(
            lesson.position for lesson in lessons
        )
        offset = max_position + len(lessons) + 1

        try:
            for lesson in lessons:
                lesson.position += offset

            self.uow.flush()

            for position, lesson_id in enumerate(
                lesson_ids, 
                start=1,
            ):
                lessons_by_id[lesson_id].position = position

            self.uow.commit()
        except Exception:
            self.uow.rollback()
            raise