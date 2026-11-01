from dataclasses import dataclass

from app.models.tag import Tag



@dataclass(frozen=True)
class TagListView:
    items: list[Tag]
    total: int
    page: int
    page_size: int
    total_pages: int