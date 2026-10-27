from uuid import UUID

from app.application.exceptions import ResourceNotFoundError
from app.application.unit_of_work import UnitOfWork



class RemoveUserTopicCommand:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def execute(
        self,
        user_id: UUID,
        topic_id: UUID
    ) -> None:

        user_topic = self.uow.user_topics.get_by_user_and_topic(
            user_id,
            topic_id,
        )

        if user_topic is None:
            raise ResourceNotFoundError(
                "Topic is not in user's interests"
            )

        try:
            self.uow.user_topics.delete(user_topic)
            self.uow.commit()
        except Exception:
            self.uow.rollback()
            raise