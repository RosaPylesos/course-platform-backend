from dataclasses import dataclass

from app.models.course import Course



@dataclass(frozen=True)
class CourseListItem:
    course: Course
    lesson_count: int