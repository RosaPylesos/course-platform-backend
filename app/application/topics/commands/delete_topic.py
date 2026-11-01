from uuid import UUID

from app.application.exceptions import (
    ConflictError,
    ResourceNotFoundError,
)
from app.application.unit_of_work import UnitOfWork



class DeleteTopicCommand:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def execute(
        self,
        topic_id: UUID
    ) -> None:

        topic = self.uow.topics.get_by_id(topic_id)

        if topic is None:
            raise ResourceNotFoundError("Topic not found")

        if self.uow.topics.has_children(topic_id):
            raise ConflictError("Cannot delete a topic that has child topics")

        if self.uow.topics.has_courses(topic_id):
            raise ConflictError("Cannot delete a topic that has courses")

        self.uow.topics.delete(topic)

        try:
            self.uow.commit()
        except Exception:
            self.uow.rollback()
            raise