from app.application.unit_of_work import UnitOfWork

from app.models.tag_category import TagCategory

from app.schemas.tag_category import TagCategoryCreate

from app.utils.slug import generate_slug



class CreateTagCategoryCommand:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def execute(
        self,
        category_data: TagCategoryCreate,
    ) -> TagCategory:

        slug = generate_slug(category_data.name)
        base_slug = slug
        counter = 2

        while self.uow.tag_categories.slug_exists(slug):
            slug = f"{base_slug}-{counter}"
            counter += 1

        category = TagCategory(
            name = category_data.name,
            slug = slug,
        )

        try:
            self.uow.tag_categories.add(category)
            self.uow.commit()
            self.uow.refresh(category)
        except Exception:
            self.uow.rollback()
            raise

        return category