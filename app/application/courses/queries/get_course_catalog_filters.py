from app.application.courses.repository import CourseRepository
from app.application.courses.views.course_catalog_filter import (
    CourseCatalogFilters,
)



class GetCourseCatalogFiltersQuery:
    def __init__(self, repository: CourseRepository) -> None:
        self.repository = repository

    def execute(self) -> CourseCatalogFilters:

        return self.repository.get_catalog_filters()