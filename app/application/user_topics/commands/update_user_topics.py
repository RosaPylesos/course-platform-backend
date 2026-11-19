from uuid import UUID

from app.application.exceptions import ResourceNotFoundError

from app.application.unit_of_work import UnitOfWork

from app.models.user_topic import UserTopic



class UpdateUserTopicsCommand:
    def __init__(self, uow = UnitOfWork) -> None:
        self.uow = uow

    def execute(
        self,
        user_id: UUID,
        topic_ids: list[UUID],
    ) -> None:

        current_user_topics = self.uow.user_topics.list_user_topics(user_id)

        current_topic_ids = {
            user_topic.topic_id
            for user_topic in current_user_topics
        }

        requested_topic_ids = set(topic_ids)

        to_add = requested_topic_ids - current_topic_ids
        to_remove = current_topic_ids - requested_topic_ids

        for topic_id in to_add:
            topic = self.uow.topics.get_by_id(topic_id)

            if topic is None:
                raise ResourceNotFoundError("Topic not found")

        try:
            for user_topic in current_user_topics:
                if user_topic.topic_id in to_remove:
                    self.uow.user_topics.delete(user_topic)

            for topic_id in to_add:
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