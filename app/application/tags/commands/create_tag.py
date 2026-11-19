from app.application.exceptions import ResourceNotFoundError
from app.application.unit_of_work import UnitOfWork

from app.models.tag import Tag

from app.schemas.tag import TagCreate

from app.utils.slug import generate_unique_slug



class CreateTagCommand:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def execute(
        self,
        tag_data: TagCreate,
    ) -> Tag:

        category = self.uow.tag_categories.get_by_id(
            tag_data.tag_category_id
        )

        if category is None:
            raise ResourceNotFoundError(
                "Tag category not found"
            )

        slug = generate_unique_slug(
            tag_data.name,
            self.uow.tags.slug_exists,
        )

        tag = Tag(
            tag_category_id=category.id,
            name = tag_data.name,
            slug = slug,
        )

        try:
            self.uow.tags.add(tag)
            self.uow.commit()
            self.uow.refresh(tag)
        except Exception:
            self.uow.rollback()
            raise

        return tag