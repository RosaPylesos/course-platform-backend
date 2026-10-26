from app.application.tags.repository import TagRepository

from app.models.tag import Tag



class GetTagsQuery:
    def __init__(self, repository: TagRepository) -> None:
        self.repository = repository

    def execute(self) -> list[Tag]:

        return self.repository.list_all()