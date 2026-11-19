from uuid import UUID

from app.application.tags.repository import TagRepository
from app.application.topics.repository import TopicRepository
from app.application.exceptions import ResourceNotFoundError



class ResolveCatalogFilters:
    def __init__(
        self,
        topic_repo: TopicRepository,
        tag_repo: TagRepository, 
    ) -> None:
        self.topic_repo = topic_repo
        self.tag_repo = tag_repo

    @staticmethod
    def _parse_slugs(value: str | None) -> list[str] | None:
        
        if not value:
            return None

        slugs = [
            slug.strip()
            for slug in value.split(",")
            if slug.strip()
        ]

        return slugs or None

    def resolve_topics(
        self,
        slugs: str | None,
    ) -> list[UUID] | None:

        parsed_slugs = self._parse_slugs(slugs)
        
        if not parsed_slugs:
            return None

        topic_ids = []

        for slug in parsed_slugs:
            topic = self.topic_repo.get_by_slug(slug)

            if topic is None:
                raise ResourceNotFoundError(
                    "Topic not found"
                )
            topic_ids.append(topic.id)

        return topic_ids

    def resolve_tags(
        self,
        slugs: list[str] | None,
    ) -> dict[UUID, list[UUID]] | None:

        parsed_slugs = self._parse_slugs(slugs)
        
        if not parsed_slugs:
            return None

        tags_ids_by_category: dict[UUID, list[UUID]] = {}

        for slug in parsed_slugs:
            tag = self.tag_repo.get_by_slug(slug)

            if tag is None:
                raise ResourceNotFoundError(
                    "Tag not found"
                )

            category_id = tag.tag_category_id
            category_tags = tags_ids_by_category.setdefault(
                category_id, []
            )

            if tag.id not in category_tags:
                category_tags.append(tag.id)

        return tags_ids_by_category