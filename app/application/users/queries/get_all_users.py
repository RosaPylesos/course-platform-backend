from dataclasses import dataclass

from app.application.users.repository import UserRepository
from app.application.users.views import AllUsersView

from app.models.user import User
from app.models.enums import SortBy, SortOrder



@dataclass(frozen=True)
class GetAllUsersInput:
    page: int
    page_size: int
    sort_by: SortBy
    sort_order: SortOrder



class GetAllUsersQuery:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def execute(
        self,
        input: GetAllUsersInput,
    ) -> AllUsersView:

        return self.user_repository.list(
            page=input.page,
            page_size=input.page_size,
            sort_by=input.sort_by,
            sort_order=input.sort_order,
        )