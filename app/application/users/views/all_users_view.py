from dataclasses import dataclass

from app.models.user import User



@dataclass(frozen=True)
class AllUsersView:
    items: list[User]
    total: int
    page: int
    page_size: int
    total_pages: int