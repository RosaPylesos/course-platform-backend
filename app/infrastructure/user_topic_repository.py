from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.application.user_topics.repository import UserTopicRepository

from app.models.topic import Topic
from app.models.user_topic import UserTopic



class SqlAlchemyUserTopicRepository(UserTopicRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_by_user(
        self,
        user_id: UUID,
    ) -> list[Topic]:

        statement = (
            select(Topic)
            .join(UserTopic, UserTopic.topic_id == Topic.id)
            .where(UserTopic.user_id == user_id)
            .order_by(Topic.name, Topic.id)
        )
        return list(self.db.scalars(statement).all())

    def list_user_topics(
        self,
        user_id: UUID,
    ) -> list[UserTopic]:

        statement = select(UserTopic).where(
            UserTopic.user_id == user_id
        )
        return list(self.db.scalars(statement).all())

    def get_by_user_and_topic(
        self,
        user_id: UUID,
        topic_id: UUID,
    ) -> UserTopic | None:

        statement = select(UserTopic).where(
            UserTopic.user_id == user_id,
            UserTopic.topic_id == topic_id,
        )
        return self.db.scalar(statement)

    def add(
        self,
        user_topic: UserTopic,
    ) -> None:

        self.db.add(user_topic)

    def delete(
        self,
        user_topic: UserTopic,
    ) -> None:

        self.db.delete(user_topic)