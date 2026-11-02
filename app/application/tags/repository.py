from typing import Protocol
from uuid import UUID

from app.application.tags.views import TagListView

from app.models.tag import Tag



class TagRepository(Protocol):

    def list(
        self,
        page: int,
        page_size: int,
        tag_category_id: UUID | None = None,
    ) -> TagListView: ...

    def list_all(
        self,
        page: int,
        page_size: int,
        tag_category_id: UUID | None = None,
    ) -> TagListView: ...

    def get_by_id(
        self, 
        tag_id: UUID
    ) ->  Tag | None: ...

    def add(self, tag: Tag) -> None: ...

    def delete(self, tag: Tag) -> None: ...

    def has_course_assignments(
        self,
        tag_id: UUID
    ) -> bool: ...

    def slug_exists(
        self,
        slug: str,
        exclude_tag_id: UUID | None = None,
    ) -> bool: ...

    def get_by_slug(self, slug: str) -> Tag | None:
        ...