from dataclasses import dataclass
from uuid import UUID

from app.models.enums import CourseDifficulty



@dataclass
class CatalogFilterAuthorView:
    id:UUID
    name:str
    surname: str | None

@dataclass
class CatalogFilterTopicView:
    id: UUID
    name: str
    parent_id: UUID | None
    slug: str

@dataclass
class CatalogFilterTagView:
    id: UUID
    name: str
    slug: str

@dataclass
class CatalogFilterTagCategoryView:
    id: UUID
    name: str
    tags: list[CatalogFilterTagView]

@dataclass
class CourseCatalogFiltersView:
    authors: list[CatalogFilterAuthorView]
    topics: list[CatalogFilterTopicView]
    tag_categories: list[CatalogFilterTagCategoryView]
    difficulties: list[CourseDifficulty]