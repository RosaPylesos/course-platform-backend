from uuid import UUID
from dataclasses import dataclass

from app.application.tags.repository import TagRepository
from app.application.tags.views import TagListView



@dataclass(frozen=True)
class GetTagsInput:
    page: int
    page_size: int
    tag_category_id: UUID | None = None



class GetTagsQuery:
    def __init__(
        self, 
        tag_repository: TagRepository,
    ) -> None:
        self.tag_repository = tag_repository

    def execute(
        self,
        input: GetTagsInput,
    ) -> TagListView:

        return self.tag_repository.list(
            page=input.page,
            page_size=input.page_size,
            tag_category_id=input.tag_category_id,
        )