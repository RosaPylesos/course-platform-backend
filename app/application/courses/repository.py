from typing import Protocol
from uuid import UUID

from app.models.course import Course



class CourseRepository(Protocol):

    def list_published(self) -> list[Course]:
        ...

    def get_by_id(self, course_id: UUID) -> Course | None:
        ...

    def add(self, course: Course) -> None:
        ...

    def delete(self, course: Course) -> None:
        ...