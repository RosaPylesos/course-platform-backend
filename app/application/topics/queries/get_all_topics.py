from dataclasses import dataclass

from app.application.topics.repository import TopicRepository
from app.application.topics.views import TopicListView

from app.models.topic import Topic



@dataclass(frozen=True)
class GetAllTopicsInput:
    page: int
    page_size: int



class GetAllTopicsQuery:
    def __init__(
        self, 
        topic_repository: TopicRepository,
    ) -> None:
        self.topic_repository = topic_repository

    def execute(
        self,
        input: GetAllTopicsInput,
    ) -> TopicListView:
        return self.topic_repository.list_all(
            page=input.page,
            page_size=input.page_size,
        )