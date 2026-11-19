from uuid import UUID

from app.application.exceptions import ResourceNotFoundError
from app.application.tag_categories.repository import TagCategoryRepository

from app.models.tag_category import TagCategory



class GetTagCategoryQuery:
    def __init__(
        self, 
        category_repository: TagCategoryRepository,
    ) -> None:
        self.category_repository = category_repository

    def execute(
        self,
        category_id: UUID,
    ) -> TagCategory:

        category = self.category_repository.get_by_id(category_id)

        if category is None:
            raise ResourceNotFoundError("Tag category not found")

        return category