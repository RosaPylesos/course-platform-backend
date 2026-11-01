from dataclasses import dataclass

from app.models.course import Course



@dataclass(frozen=True)
class CourseListItemView:
    course: Course
    lesson_count: int



@dataclass(frozen=True)
class CourseListView:
    items: list[CourseListItemView]
    total: int
    page: int
    page_size: int
    total_pages: int