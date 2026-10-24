from typing import Protocol
from uuid import UUID

from app.models.lesson import Lesson



class LessonRepository(Protocol):

    def list_by_course(
        self, 
        course_id: UUID
    ) -> list[Lesson]:
        ...

    def get_by_id_for_course(
        self,
        lesson_id: UUID,
        course_id: UUID,
    ) -> Lesson | None:
        ...

    def count_by_course(
        self,
        course_id: UUID
    ) -> int:
        ...

    def get_max_position_by_course(
        self,
        course_id: UUID,
    ) -> int | None:
        ...

    def add(self, lesson: Lesson) -> None:
        ...

    def delete(self, lesson: Lesson) -> None:
        ...