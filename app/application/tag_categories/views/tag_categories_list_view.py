from dataclasses import dataclass

from app.models.tag_category import TagCategory



@dataclass(frozen=True)
class TagCategoryListView:
    items: list[TagCategory]
    total: int
    page: int
    page_size: int
    total_pages: int