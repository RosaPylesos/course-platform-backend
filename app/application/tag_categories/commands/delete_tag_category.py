from uuid import UUID

from app.application.exceptions import (
    ConflictError,
    ResourceNotFoundError,
)
from app.application.unit_of_work import UnitOfWork



class DeleteTagCategoryCommand:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def execute(
        self,
        category_id: UUID,
    ) -> None:

        category = self.uow.tag_categories.get_by_id(category_id)

        if category is None:
            raise ResourceNotFoundError("Tag category not found")

        if self.uow.tag_categories.has_tags(category_id):
            raise ConflictError(
                "Cannot delete a tag category that contains tags"
            )

        try:
            self.uow.tag_categories.delete(category)
            self.uow.commit()
        except Exception:
            self.uow.rollback()
            raise