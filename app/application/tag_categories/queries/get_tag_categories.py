from uuid import UUID
from dataclasses import dataclass

from app.application.tag_categories.repository import TagCategoryRepository

from app.models.tag_category import TagCategory



@dataclass(frozen=True)
class GetTagCategoriesInput:
    page: int
    page_size: int



class GetTagCategoriesQuery:
    def __init__(
        self, 
        category_repository: TagCategoryRepository,
    ) -> None:
        self.category_repository = category_repository

    def execute(
        self,
        input: GetTagCategoriesInput,
    ) -> list[TagCategory]:
        
        return self.category_repository.list(
            page=input.page,
            page_size=input.page_size,
        )