from app.application.courses.repository import CourseRepository

from app.models.course import Course



class GetCoursesQuery:
    def __init__(self, repository: CourseRepository) -> None:
        self.repository = repository

    def execute(self) -> list[Course]:
        return self.repository.list_published()