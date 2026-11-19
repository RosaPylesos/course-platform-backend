from uuid import UUID

from app.application.exceptions import ResourceNotFoundError
from app.application.topics.repository import TopicRepository

from app.models.topic import Topic



class GetTopicQuery:
    def __init__(
        self, 
        topic_repository: TopicRepository,
    ) -> None:
        self.topic_repository = topic_repository

    def execute(self, topic_id: UUID) -> Topic:
        
        topic = self.topic_repository.get_by_id(topic_id)

        if topic is None:
            raise ResourceNotFoundError("Topic not found")

        return topic