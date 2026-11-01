from app.application.courses.repository import CourseRepository
from app.application.courses.views.course_catalog_filter import (
    CourseCatalogFiltersView,
)



class GetCourseCatalogFiltersQuery:
    def __init__(
        self, 
        course_repository: CourseRepository,
    ) -> None:
        self.course_repository = course_repository

    def execute(self) -> CourseCatalogFiltersView:

        return self.course_repository.get_catalog_filters()