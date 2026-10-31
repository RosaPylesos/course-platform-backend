from dataclasses import dataclass

from app.models.course import Course
from app.models.enums import CourseStatus



@dataclass(frozen=True)
class MyCoursesView:
    items: list[Course]
    total: int
    page: int
    page_size: int
    total_pages: int
    status_counts: dict[CourseStatus, int]