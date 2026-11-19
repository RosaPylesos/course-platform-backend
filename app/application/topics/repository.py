from typing import Protocol
from uuid import UUID

from app.application.topics.views import (
    TopicListView, 
)

from app.models.topic import Topic



class TopicRepository(Protocol):
    
    def list(self) -> list[Topic]:
        ...

    def list_all(
        self,
        page: int,
        page_size: int,
    ) -> TopicListView:
        ...

    def get_by_id(
        self, 
        topic_id: UUID,
    ) -> Topic | None:
        ...

    def add(
        self, 
        topic: Topic,
    ) -> None:
        ...

    def delete(
        self,
        topic: Topic,
    ) -> None:
        ...

    def has_children(
        self, 
        topic_id:UUID,
    ) -> bool:
        ...

    def has_courses(
        self,
        topic_id: UUID
    ) -> bool:
        ...

    def slug_exists(
        self,
        slug: str,
        exclude_topic_id: UUID | None = None,
    ) -> bool:
        ...

    def get_by_slug(
        self,
        slug: str,
    ) -> Topic | None:
        ...