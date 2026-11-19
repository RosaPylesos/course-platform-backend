from dataclasses import dataclass
from uuid import UUID



@dataclass(frozen=True)
class PublicTagView:
    id: UUID
    name: str
    slug: str

@dataclass(frozen=True)
class PublicTagCategoryView:
    id: UUID
    name: str
    tags: list[PublicTagView]