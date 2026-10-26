from uuid import UUID

from app.application.exceptions import (
    InvalidInputError,
    ResourceNotFoundError,
)
from app.application.unit_of_work import UnitOfWork

from app.models.tag import Tag

from app.schemas.tag import TagUpdate

from app.utils.slug import generate_slug



class UpdateTagCommand:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def exeucte(
        self,
        tag_id: UUID,
        tag_data: TagUpdate
    ) -> Tag:

        tag = self.uow.tags.get_by_id(tag_id)

        if tag is None:
            raise ResourceNotFoundError("Tag not found")

        update_data = tag_data.model_dump(exclude_unset=True)

        if "name" in update_data:
            new_name = update_data.pop("name")

            if new_name is None:
                raise InvalidInputError("Tag name cannot be null")

            slug = generate_slug(new_name)
            base_slug = slug
            counter = 2

            while self.uow.tags.slug_exists(
                slug,
                exclude_tag_id=tag_id,
            ):
                slug = f"{base_slug}-{counter}"
                counter += 1

            tag.name = new_name
            tag.slug = slug

        if "tag_category_id" in update_data:
            category_id = update_data["tag_category_id"]

            if category_id is None:
                raise InvalidInputError("Tag category cannot be null")

            category = self.uow.tag_categories.get_by_id(category_id)

            if category is None:
                raise ResourceNotFoundError("Tag category not found")

        for field, value in update_data.items():
            setattr(tag, field, value)

        try:
            self.uow.commit()
            self.uow.refresh(tag)
        except Exception:
            self.uow.rollback()
            raise

        return tag