from app.application.tag_categories.repository import TagCategoryRepository

from app.models.tag_category import TagCategory



class GetTagCategoriesQuery:
    def __init__(
        self, 
        category_repository: TagCategoryRepository
    ) -> None:
        self.category_repository = category_repository

    def execute(self) -> list[TagCategory]:

        return self.category_repository.list_public()