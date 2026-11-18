from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.orm import Session, selectinload

from app.application.tag_categories.repository import TagCategoryRepository
from app.application.tag_categories.views import (
    TagCategoryListView,
    PublicTagCategoryView,
    PublicTagView,
)

from app.models.tag_category import TagCategory
from app.models.tag import Tag



class SqlAlchemyTagCategoryRepository(TagCategoryRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_public(self) -> list[TagCategory]:

        statement = (
            select(TagCategory)
            .order_by(TagCategory.name, TagCategory.id)
        )

        return list(
            self.db.scalars(statement).all()
        )

    def list_all_with_tags(self) -> list[PublicTagCategoryView]:

        statement = (
            select(TagCategory)
            .options(selectinload(TagCategory.tags))
            .order_by(TagCategory.name, TagCategory.id)
        )

        categories = self.db.scalars(statement).all()

        return [
            PublicTagCategoryView(
                id=category.id,
                name=category.name,
                tags=[
                    PublicTagView(
                        id=tag.id,
                        name=tag.name,
                        slug=tag.slug,
                    )
                    for tag in sorted(
                        category.tags,
                        key=lambda item: (item.name, item.id)
                    )
                ],
            ) 
            for category in categories
        ]

    def list_all(
        self,
        page: int,
        page_size: int,
    ) -> TagCategoryListView:
        
        offset = (page - 1) * page_size

        statement = (
            select(TagCategory)
            .order_by(TagCategory.name, TagCategory.id)
            .offset(offset)
            .limit(page_size)
        )

        items = list(self.db.scalars(statement).all())

        total_statement = select(
            func.count(TagCategory.id)
        )

        total = self.db.scalar(total_statement) or 0

        return TagCategoryListView(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=(total + page_size - 1) // page_size
        )

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
        exclude_id: UUID | None = None,
    ) -> bool:

        statement = select(TagCategory.id).where(
            TagCategory.slug == slug
        )

        if exclude_id is not None:
            statement = statement.where(
                TagCategory.id != exclude_id
            )
        return self.db.scalar(statement) is not None