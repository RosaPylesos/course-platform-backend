from dataclasses import dataclass

from app.application.courses.repository import CourseRepository
from app.application.courses.views import AllCoursesView

from app.models.course import Course
from app.models.enums import SortBy, SortOrder



@dataclass(frozen=True)
class GetAllCoursesInput:
    page: int
    page_size: int
    sort_by: SortBy
    sort_order: SortOrder



class GetAllCoursesQuery:
    def __init__(
        self, 
        course_repository: CourseRepository,
    ) -> None:
        self.course_repository = course_repository

    def execute(
        self,
        input: GetAllCoursesInput,
    ) -> AllCoursesView:

        return self.course_repository.list_all(
            page=input.page,
            page_size=input.page_size,
            sort_by=input.sort_by,
            sort_order=input.sort_order
        )