from dataclasses import dataclass

from app.application.courses.views import CourseListItem

from app.models.topic import Topic

@dataclass(frozen=True)
class HomePageSection:
    topic: Topic
    courses: list[CourseListItem]