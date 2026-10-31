from uuid import UUID

from app.application.users.repository import UserRepository

from app.models.user import User

from app.application.exceptions import ResourceNotFoundError



class GetMyProfileQuery:
    def __init__(
        self,
        user_repository: UserRepository,
    ) -> None:
        self.user_repository = user_repository

    def execute(
        self,
        user_id: UUID,
    ) -> User:

        user = self.user_repository.get_profile_by_id(user_id)

        if user is None:
            raise ResourceNotFoundError("User not found")

        return user