from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.application.tags.repository import TagRepository

from app.models.tag import Tag
from app.models.course_tag import CourseTag



class SqlAlchemyTagRepository(TagRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_all(self) -> list[Tag]:

        statement = select(Tag).order_by(Tag.name)
        return list(self.db.scalars(statement).all())

    def get_by_id(
        self,
        tag_id: UUID,
    ) -> Tag | None:

        return self.db.get(Tag, tag_id)

    def add(
        self,
        tag: Tag,
    ) -> None:

        self.db.add(tag)

    def delete(
        self,
        tag: Tag,
    ) -> None:

        self.db.delete(tag)

    def has_course_assignments(
        self,
        tag_id: UUID,
    ) -> bool:

        statement = (
            select(CourseTag.tag_id)
            .where(CourseTag.tag_id == tag_id)
            .limit(1)
        )
        return self.db.scalar(statement) is not None

    def slug_exists(
        self,
        slug: str,
        exclude_tag_id: UUID | None = None,
    ) -> bool:

        statement = select(Tag.id).where(Tag.slug == slug)

        if exclude_tag_id is not None:
            statement = statement.where(Tag.id != exclude_tag_id)

        return self.db.scalar(statement) is not None