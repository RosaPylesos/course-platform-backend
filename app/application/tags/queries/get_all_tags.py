from uuid import UUID
from dataclasses import dataclass

from app.application.tags.repository import TagRepository
from app.application.tags.views import TagListView



@dataclass(frozen=True)
class GetAllTagsInput:
    page: int
    page_size: int
    tag_category_id: UUID | None = None



class GetAllTagsQuery:
    def __init__(
        self, 
        tag_repository: TagRepository,
    ) -> None:
        self.tag_repository = tag_repository

    def execute(
        self,
        input: GetAllTagsInput,
    ) -> TagListView:

        return self.tag_repository.list_all(
            page=input.page,
            page_size=input.page_size,
            tag_category_id=input.tag_category_id,
        )