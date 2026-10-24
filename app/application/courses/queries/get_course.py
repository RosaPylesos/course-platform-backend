from uuid import UUID

from app.application.courses.repository import CourseRepository
from app.application.exceptions import (
    AccessDeniedError,
    ResourceNotFoundError
)

from app.models.course import Course
from app.models.enums import CourseStatus



class GetCourseQuery:
    def __init__(self, repository: CourseRepository) -> None:
        self.repository = repository

    def execute(
        self,
        course_id: UUID
    ) -> Course:

        course = self.repository.get_by_id(course_id)

        if course is None:
            raise ResourceNotFoundError("Course not found")

        if course.status != CourseStatus.PUBLISHED:
            raise AccessDeniedError(
                "This course is not published yet"
            )

        return course