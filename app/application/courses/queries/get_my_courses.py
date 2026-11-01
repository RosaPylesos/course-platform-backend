from uuid import UUID
from dataclasses import dataclass

from app.application.courses.repository import CourseRepository
from app.application.courses.views import MyCoursesView

from app.models.enums import CourseStatus



@dataclass(frozen=True)
class GetMyCoursesInput:
    page: int = 1
    page_size: int = 16
    status: CourseStatus | None = None



class GetMyCoursesQuery:
    def __init__(
        self, 
        course_repository: CourseRepository,
    ) -> None:
        self.course_repository = course_repository

    def execute(
        self,
        author_id: UUID,
        input: GetMyCoursesInput
    ) -> MyCoursesView:

        return self.course_repository.list_by_author(
            author_id=author_id,
            page=input.page,
            page_size=input.page_size,
            status=input.status,
        )