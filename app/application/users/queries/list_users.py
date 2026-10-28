from app.application.users.repository import UserRepository

from app.models.user import User



class ListUsersQuery:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def execute(self) -> list[User]:

        return self.repository.list_all()