from app.application.topics.repository import TopicRepository

from app.models.topic import Topic



class GetTopicsQuery:
    def __init__(self, repository: TopicRepository) -> None:
        self.repository = repository

    def execute(self) -> list[Topic]:
        return self.repository.list_all()