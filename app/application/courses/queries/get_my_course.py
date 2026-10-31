from uuid import UUID

from app.application.courses.repository import CourseRepository
from app.application.exceptions import (
    AccessDeniedError,
    ResourceNotFoundError,
)

from app.models.course import Course



class GetMyCourseQuery:
    def __init__(self, repository: CourseRepository) -> None:
        self.repository = repository

    def execute(
        self,
        course_id: UUID,
        author_id: UUID,
    ) -> Course:

        course = self.repository.get_by_id_with_relations(
            course_id
        )

        if course is None:
            raise ResourceNotFoundError("Course not found")

        if course.author_id != author_id:
            raise AccessDeniedError(
                "You do not have access to this course"
            )

        return course