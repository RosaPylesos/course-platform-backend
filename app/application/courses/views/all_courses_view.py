from dataclasses import dataclass

from app.models.course import Course



@dataclass(frozen=True)
class AllCoursesView:
    items: list[Course]
    total: int
    page: int
    page_size: int
    total_pages: int