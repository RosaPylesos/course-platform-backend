from uuid import UUID

from app.application.exceptions import (
    InvalidInputError,
    ResourceNotFoundError,
)
from app.application.unit_of_work import UnitOfWork

from app.models.topic import Topic

from app.schemas.topic import TopicUpdate

from app.utils.slug import generate_slug



class UpdateTopicCommand:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def execute(
        self,
        topic_id: UUID,
        topic_data: TopicUpdate,
    ) -> Topic:
        
        topic = self.uow.topics.get_by_id(topic_id)

        if topic is None:
            raise ResourceNotFoundError("Topic not found")

        update_data = topic_data.model_dump(exclude_unset=True)

        if "name" in update_data:
            new_name = update_data.pop("name")

            if new_name is None:
                raise InvalidInputError("Topic name cannot be null")

            slug = generate_slug(new_name)
            base_slug = slug
            counter = 2

            while self.uow.topics.slug_exists(
                slug,
                exclude_topic_id=topic_id
            ):
                slug = f"{base_slug}-{counter}"
                counter += 1

            topic.name = new_name
            topic.slug = slug

        for field, value in update_data.items():
            setattr(topic, field, value)

        self.uow.commit()
        self.uow.refresh(topic)

        return topic