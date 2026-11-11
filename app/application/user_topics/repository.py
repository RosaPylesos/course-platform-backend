from typing import Protocol
from uuid import UUID

from app.models.user_topic import UserTopic
from app.models.topic import Topic



class UserTopicRepository(Protocol):

    def list_by_user(
        self,
        user_id: UUID,
    ) -> list[Topic]:
        ...

    def list_user_topics(
        self,
        user_id: UUID,
    ) -> list[UserTopic]:
        ...

    def get_by_user_and_topic(
        self,
        user_id: UUID,
        topic_id: UUID,
    ) -> UserTopic | None:
        ...

    def add(
        self,
        user_topic: UserTopic,
    ) -> None:
        ...

    def delete(
        self,
        user_topic: UserTopic,
    ) -> None:
        ...