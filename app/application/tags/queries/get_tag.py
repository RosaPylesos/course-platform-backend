from uuid import UUID

from app.application.exceptions import ResourceNotFoundError
from app.application.tags.repository import TagRepository

from app.models.tag import Tag



class GetTagQuery:
    def __init__(self, repository: TagRepository) -> None:
        self.repository = repository

    def execute(
        self,
        tag_id: UUID,
    ) -> Tag:

        tag = self.repository.get_by_id(tag_id)

        if tag is None:
            raise ResourceNotFoundError("Tag not found")

        return tag