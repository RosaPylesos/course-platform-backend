from app.application.tag_categories.repository import TagCategoryRepository
from app.application.tag_categories.views import PublicTagCategoryView



class GetTagCategoriesQuery:
    def __init__(
        self, 
        category_repository: TagCategoryRepository,
    ) -> None:
        self.category_repository = category_repository

    def execute(self) -> list[PublicTagCategoryView]:
        
        return self.category_repository.list_all_with_tags()