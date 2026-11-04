from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.application.topics.repository import TopicRepository
from app.application.topics.views import (
    TopicListView,
)

from app.models.topic import Topic
from app.models.course import Course



class SqlAlchemyTopicRepository(TopicRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def list(self) -> list[Topic]:

        statement = (
            select(Topic)
            .order_by(Topic.name, Topic.id)
        )

        return list(
            self.db.scalars(statement).all()
        )

    def list_all(
        self,
        page: int,
        page_size: int,
    ) -> TopicListView:

        offset = (page - 1) * page_size

        statement = (
            select(Topic)
            .order_by(Topic.name, Topic.id)
            .offset(offset)
            .limit(page_size)
        )

        items = list(self.db.scalars(statement).all())

        total_statement = select(
            func.count(Topic.id)
        )

        total = self.db.scalar(total_statement) or 0

        return TopicListView(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=(total + page_size - 1) // page_size
        )

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
        exclude_id: UUID | None = None,
    ) -> bool:

        statement = select(Topic.id).where(Topic.slug == slug)

        if exclude_id is not None:
            statement = statement.where(Topic.id != exclude_id)

        return self.db.scalar(statement) is not None

    def get_by_slug(
        self,
        slug: str,
    ) -> Topic | None:
        statement = select(Topic).where(Topic.slug == slug)
        return self.db.scalar(statement)