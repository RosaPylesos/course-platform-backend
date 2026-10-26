from app.application.exceptions import ResourceNotFoundError
from app.application.unit_of_work import UnitOfWork

from app.models.topic import Topic

from app.schemas.topic import TopicCreate

from app.utils.slug import generate_slug



class CreateTopicCommand:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def execute(
        self,
        topic_data: TopicCreate,
    ) -> Topic:

        if topic_data.parent_id is not None:
            parent = self.uow.topics.get_by_id(
                topic_data.parent_id
            )

            if parent is None:
                raise ResourceNotFoundError(
                    "Parent topic not found"
                )

        slug = generate_slug(topic_data.name)
        base_slug = slug
        counter = 2

        while self.uow.topics.slug_exists(slug):
            slug = f"{base_slug}-{counter}"
            counter += 1

        topic = Topic(
            name = topic_data.name,
            parent_id = topic_data.parent_id,
            slug = slug
        )

        self.uow.topics.add(topic)
        self.uow.commit()
        self.uow.refresh(topic)

        return topic