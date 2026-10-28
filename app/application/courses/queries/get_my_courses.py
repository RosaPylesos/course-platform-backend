from uuid import UUID

from app.application.courses.repository import CourseRepository

from app.models.course import Course



class GetMyCoursesQuery:
    def __init__(self, repository: CourseRepository) -> None:
        self.repository = repository

    def execute(
        self,
        author_id: UUID
    ) -> list[Course]:

        return self.repository.list_by_author(author_id)