from uuid import UUID

from app.application.exceptions import (
    ConflictError,
    ResourceNotFoundError,
)
from app.application.unit_of_work import UnitOfWork



class DeleteTagCommand:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def execute(
        self,
        tag_id: UUID
    ) -> None:

        tag = self.uow.tags.get_by_id(tag_id)

        if tag is None:
            raise ResourceNotFoundError("Tag not found")

        if self.uow.tags.has_course_assignments(tag_id):
            raise ConflictError(
                "Cannot delete a tag assigned to courses"
            )

        try:
            self.uow.tags.delete(tag)
            self.uow.commit()
        except Exception:
            self.uow.rollback()
            raise