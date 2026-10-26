from app.application.tag_categories.repository import TagCategoryRepository

from app.models.tag_category import TagCategory



class GetTagCategoriesQuery:
    def __init__(self, repository: TagCategoryRepository) -> None:
        self.repository = repository

    def execute(self) -> list[TagCategory]:
        return self.repository.list_all()