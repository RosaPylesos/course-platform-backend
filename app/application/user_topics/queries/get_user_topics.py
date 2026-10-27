from uuid import UUID

from app.application.user_topics.repository import UserTopicRepository

from app.models.topic import Topic



class GetUserTopicsQuery:
    def __init__(self, repository: UserTopicRepository) -> None:
        self.repository = repository

    def execute(
        self,
        user_id: UUID,
    ) -> list[Topic]:

        return self.repository.list_by_user(user_id)