from dataclasses import dataclass

from app.application.courses.views import CourseListItemView

from app.models.topic import Topic

@dataclass(frozen=True)
class HomePageSectionView:
    topic: Topic
    courses: list[CourseListItemView]