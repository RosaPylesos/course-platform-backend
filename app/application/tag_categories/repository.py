from typing import Protocol
from uuid import UUID

from app.models.tag_category import TagCategory



class TagCategoryRepository(Protocol):
    
    def list(
        self,
        page: int,
        page_size: int,
    ) -> tuple[list[TagCategory], int]:
        ...

    def get_by_id(
        self,
        category_id: UUID,
    ) -> TagCategory | None:
        ...

    def add(
        self,
        category: TagCategory,
    ) -> None:
        ...

    def delete(
        self,
        category: TagCategory,
    ) -> None:
        ...

    def has_tags(
        self,
        category_id: UUID,
    ) -> bool:
        ...

    def slug_exists(
        self,
        slug: str,
        exclude_category_id: UUID | None = None,
    ) -> bool:
        ...