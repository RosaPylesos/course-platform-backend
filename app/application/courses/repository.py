from typing import Protocol
from uuid import UUID

from app.models.course import Course



class CourseRepository(Protocol):

    def get_by_id(self, course_id: UUID) -> Course | None:
        ...