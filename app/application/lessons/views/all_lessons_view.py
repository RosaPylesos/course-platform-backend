from dataclasses import dataclass

from app.models.lesson import Lesson



@dataclass(frozen=True)
class AllLessonsView:
    items: list[Lesson]
    total: int
    page: int
    page_size: int
    total_pages: int