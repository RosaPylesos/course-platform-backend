from dataclasses import dataclass

from app.application.tag_categories.repository import (
    TagCategoryRepository,
)
from app.application.tag_categories.views import (
    TagCategoryListView,
)



@dataclass(frozen=True)
class GetAllTagCategoriesInput:
    page: int
    page_size: int



class GetAllTagCategoriesQuery:
    def __init__(
        self, 
        category_repository: TagCategoryRepository,
    ) -> None:
        self.category_repository = category_repository

    def execute(
        self,
        input: GetAllTagCategoriesInput,
    ) -> TagCategoryListView:
        
        return self.category_repository.list_all(
            page=input.page,
            page_size=input.page_size,
        )