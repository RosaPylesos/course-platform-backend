from dataclasses import dataclass

from app.models.topic import Topic



@dataclass(frozen=True)
class TopicListView:
    items: list[Topic]
    total: int
    page: int
    page_size: int
    total_pages: int