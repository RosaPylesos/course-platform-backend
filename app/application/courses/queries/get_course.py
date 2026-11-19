from uuid import UUID

from app.application.courses.repository import CourseRepository
from app.application.exceptions import (
    AccessDeniedError,
    ResourceNotFoundError
)
from app.application.courses.views.course_list import (
    CourseListItemView
)

from app.models.enums import CourseStatus



class GetCourseQuery:
    def __init__(
        self, 
        course_repository: CourseRepository,
    ) -> None:
        self.course_repository = course_repository

    def execute(
        self,
        course_id: UUID
    ) -> CourseListItemView:
        course = self.course_repository.get_detail(course_id)

        if course is None:
            raise ResourceNotFoundError("Course not found")

        if course.course.status != CourseStatus.PUBLISHED:
            raise AccessDeniedError(
                "This course is not published yet"
            )

        return course