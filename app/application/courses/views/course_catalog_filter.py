from dataclasses import dataclass
from uuid import UUID

from app.models.enums import CourseDifficulty



@dataclass
class CatalogFilterAuthor:
    id:UUID
    name:str
    surname: str | None

@dataclass
class CatalogFilterTopic:
    id: UUID
    name: str
    parent_id: UUID | None
    slug: str

@dataclass
class CatalogFilterTag:
    id: UUID
    name: str
    slug: str

@dataclass
class CatalogFilterTagCategory:
    id: UUID
    name: str
    tags: list[CatalogFilterTag]

@dataclass
class CourseCatalogFilters:
    authors: list[CatalogFilterAuthor]
    topics: list[CatalogFilterTopic]
    tag_categories: list[CatalogFilterTagCategory]
    difficulties: list[CourseDifficulty]