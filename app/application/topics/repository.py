from typing import Protocol
from uuid import UUID

from app.models.topic import Topic



class TopicRepository(Protocol):
    
    def list_all(self) -> list[Topic]:
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