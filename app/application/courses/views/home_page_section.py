from uuid import UUID
from dataclasses import dataclass

from app.application.courses.views import CourseListItemView

@dataclass(frozen=True)
class HomePageTopicView:
    id: UUID
    parent_id: UUID | None
    name: str
    slug: str
    has_children: bool

@dataclass(frozen=True)
class HomePageSectionView:
    topic: HomePageTopicView
    courses: list[CourseListItemView]