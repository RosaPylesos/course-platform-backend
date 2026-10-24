from typing import Protocol
from uuid import UUID

from app.models.lesson_progress import LessonProgress



class LessonProgressRepository(Protocol):

    def get_by_enrollment_and_lesson(
        self,
        enrollment_id: UUID,
        lesson_id: UUID
    ) -> LessonProgress | None:
        ...
    
    def count_completed_by_enrollment(
        self,
        enrollment_id: UUID,
    ) -> int:
        ...

    def add(self, progress: LessonProgress) -> None:
        ...