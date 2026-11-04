from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.application.tags.repository import TagRepository
from app.application.tags.views import TagListView

from app.models.tag import Tag
from app.models.course_tag import CourseTag



class SqlAlchemyTagRepository(TagRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_all(
        self,
        page: int,
        page_size: int,
        tag_category_id: UUID | None = None,
    ) -> TagListView:

        offset = (page - 1) * page_size

        statement = select(Tag)

        total_statement = select(func.count(Tag.id))

        if tag_category_id is not None:
            statement = statement.where(
                Tag.tag_category_id == tag_category_id
            )

            total_statement = total_statement.where(
                Tag.tag_category_id == tag_category_id
            )

        statement = (
            statement
            .order_by(Tag.name, Tag.id)
            .offset(offset)
            .limit(page_size)
        )

        items = list(self.db.scalars(statement).all())
        total = self.db.scalar(total_statement) or 0

        return TagListView(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=(total + page_size - 1) // page_size
        )

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
        exclude_id: UUID | None = None,
    ) -> bool:

        statement = select(Tag.id).where(Tag.slug == slug)

        if exclude_id is not None:
            statement = statement.where(Tag.id != exclude_id)

        return self.db.scalar(statement) is not None

    def get_by_slug(self, slug: str) -> Tag | None:

        statement = select(Tag).where(Tag.slug == slug)
        return self.db.scalar(statement)