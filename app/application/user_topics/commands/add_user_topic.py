from uuid import UUID

from app.application.exceptions import (
    ConflictError,
    ResourceNotFoundError,
)
from app.application.unit_of_work import UnitOfWork

from app.models.user_topic import UserTopic



class AddUserTopicCommand:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def execute(
        self,
        user_id: UUID,
        topic_id: UUID,
    ) -> None:

        topic = self.uow.topics.get_by_id(topic_id)

        if topic is None:
            raise ResourceNotFoundError("Topic not found")

        existing = self.uow.user_topics.get_by_user_and_topic(
            user_id,
            topic_id,
        )

        if existing is not None:
            raise ConflictError(
                "Topic is already in user's interests"
            )


        try:
            self.uow.user_topics.add(
                UserTopic(
                    user_id=user_id,
                    topic_id=topic_id,
                )
            )
            self.uow.commit()
        except Exception:
            self.uow.rollback()
            raise