from uuid import UUID

from app.application.exceptions import (
    InvalidInputError,
    ResourceNotFoundError,
)
from app.application.unit_of_work import UnitOfWork

from app.models.tag_category import TagCategory

from app.schemas.tag_category import TagCategoryUpdate

from app.utils.slug import generate_unique_slug



class UpdateTagCategoryCommand:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def execute(
        self,
        category_id: UUID,
        category_data: TagCategoryUpdate,
    ) -> TagCategory:

        category = self.uow.tag_categories.get_by_id(category_id)

        if category is None:
            raise ResourceNotFoundError("Tag category not found")

        update_data = category_data.model_dump(exclude_unset=True)

        if not update_data:
            raise InvalidInputError("No fields to update")

        if "name" in update_data:
            new_name = update_data.pop("name")

            if new_name is None:
                raise InvalidInputError("Tag category name cannot be null")

            slug = generate_unique_slug(
                new_name,
                self.uow.tag_categories.slug_exists,
                exclude_id=category_id,
            )

            category.name = new_name
            category.slug = slug

        for field, value in update_data.items():
            setattr(category, field, value)

        try:
            self.uow.commit()
            self.uow.refresh(category)
        except Exception:
            self.uow.rollback()
            raise

        return category