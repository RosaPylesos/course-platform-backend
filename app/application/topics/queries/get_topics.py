from uuid import UUID

from app.application.topics.repository import TopicRepository
from app.application.topics.views import PublicTopicView

from app.models.topic import Topic



class GetTopicsQuery:
    def __init__(
        self, 
        topic_repository: TopicRepository,
    ) -> None:
        self.topic_repository = topic_repository

    def execute(self) -> list[PublicTopicView]:

        topics = self.topic_repository.list()

        children_by_parent: dict[
            UUID | None, 
            list[Topic],
        ] = {}

        for topic in topics:
            children_by_parent.setdefault(
                topic.parent_id,
                [],
            ).append(topic)

        def build_topic(
            topic: Topic,
        ) -> PublicTopicView:

            return PublicTopicView(
                id=topic.id,
                name=topic.name,
                slug=topic.slug,
                children=[
                    build_topic(child)
                    for child in children_by_parent.get(
                        topic.id,
                        [],
                    )
                ],
            )
        
        return [
            build_topic(topic)
            for topic in children_by_parent.get(None, [])
        ]