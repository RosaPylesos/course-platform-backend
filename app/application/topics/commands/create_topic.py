from app.application.exceptions import ResourceNotFoundError
from app.application.unit_of_work import UnitOfWork

from app.models.topic import Topic

from app.schemas.topic import TopicCreate

from app.utils.slug import generate_unique_slug



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

        slug = generate_unique_slug(
            topic_data.name,
            self.uow.topics.slug_exists,
        )

        topic = Topic(
            name = topic_data.name,
            parent_id = topic_data.parent_id,
            slug = slug
        )

        try:
            self.uow.topics.add(topic)
            self.uow.commit()
            self.uow.refresh(topic)
        except Exception:
            self.uow.rollback()
            raise

        return topic