from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.application.tag_categories.repository import TagCategoryRepository

from app.models.tag_category import TagCategory
from app.models.tag import Tag



class SqlAlchemyTagCategoryRepository(TagCategoryRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_all(self) -> list[TagCategory]:

        statement = select(TagCategory).order_by(TagCategory.name)
        return list(self.db.scalars(statement).all())

    def get_by_id(
        self,
        category_id: UUID,
    ) -> TagCategory | None:

        return self.db.get(TagCategory, category_id)

    def add(
        self,
        category: TagCategory,
    ) -> None:

        self.db.add(category)

    def delete(
        self,
        category: TagCategory,
    ) -> None:

        self.db.delete(category)

    def has_tags(
        self,
        category_id: UUID,
    ) -> bool:

        statement = (
            select(Tag.id)
            .where(Tag.tag_category_id == category_id)
            .limit(1)
        )
        return self.db.scalar(statement) is not None

    def slug_exists(
        self,
        slug: str,
        exclude_category_id: UUID | None = None,
    ) -> bool:

        statement = select(TagCategory.id).where(
            TagCategory.slug == slug
        )

        if exclude_category_id is not None:
            statement = statement.where(
                TagCategory.id != exclude_category_id
            )
        return self.db.scalar(statement) is not None