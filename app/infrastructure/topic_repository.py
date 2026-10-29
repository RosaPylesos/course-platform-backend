from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.application.topics.repository import TopicRepository

from app.models.topic import Topic
from app.models.course import Course



class SqlAlchemyTopicRepository(TopicRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_all(self) -> list[Topic]:

        statement = select(Topic).order_by(Topic.name)
        return list(self.db.scalars(statement).all())

    def get_by_id(
        self, 
        topic_id: UUID,
    ) -> Topic | None:
        
        return self.db.get(Topic, topic_id)

    def add(
        self,
        topic: Topic,
    ) -> None:
        self.db.add(topic)

    def delete(
        self,
        topic: Topic,
    ) -> None:
        self.db.delete(topic)

    def has_children(
        self,
        topic_id: UUID,
    ) -> bool:

        statement = (
            select(Topic.id)
            .where(Topic.parent_id == topic_id)
            .limit(1)
        )
        return self.db.scalar(statement) is not None

    def has_courses(
        self,
        topic_id: UUID,
    ) -> bool:

        statement = (
            select(Course.id)
            .where(Course.topic_id == topic_id)
            .limit(1)
        )
        return self.db.scalar(statement) is not None

    def slug_exists(
        self,
        slug: str,
        exclude_topic_id: UUID | None = None,
    ) -> bool:

        statement = select(Topic.id).where(Topic.slug == slug)

        if exclude_topic_id is not None:
            statement = statement.where(Topic.id != exclude_topic_id)

        return self.db.scalar(statement) is not None

    def get_by_slug(
        self,
        slug: str,
    ) -> Topic | None:
        statement = select(Topic).where(Topic.slug == slug)
        return self.db.scalar(statement)