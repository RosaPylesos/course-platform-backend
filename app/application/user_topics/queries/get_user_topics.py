from uuid import UUID

from app.application.user_topics.repository import UserTopicRepository

from app.models.topic import Topic



class GetUserTopicsQuery:
    def __init__(
        self, 
        user_topic_repository: UserTopicRepository,
    ) -> None:
        self.user_topic_repository = user_topic_repository

    def execute(
        self,
        user_id: UUID,
    ) -> list[Topic]:

        return self.user_topic_repository.list_by_user(user_id)