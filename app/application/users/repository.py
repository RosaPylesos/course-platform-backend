from typing import Protocol
from uuid import UUID

from app.application.users.views import AllUsersView

from app.models.user import User
from app.models.enums import SortBy, SortOrder



class UserRepository(Protocol):

    def get_by_id(
        self,
        user_id: UUID
    ) -> User | None:
        ...

    def get_profile_by_id(
        self,
        user_id: UUID,
    ) -> User | None:
        ...

    def get_by_email(
        self, 
        email: str,
    ) -> User | None:
        ...

    def list(
        self,
        page: int,
        page_size: int,
        sort_by: SortBy,
        sort_order: SortOrder,
    ) -> AllUsersView:
        ...

    def add(
        self,
        user: User
    ) -> None:
        ...