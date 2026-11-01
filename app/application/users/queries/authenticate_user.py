from app.application.exceptions import InvalidCredentialsError
from app.application.users.repository import UserRepository

from app.core.security import create_access_token, verify_password

from app.models.user import User



class AuthenticateUserQuery:
    def __init__(
        self, 
        user_repository: UserRepository,
    ) -> None:
        self.user_repository = user_repository

    def execute(
        self,
        email: str,
        password: str,
    ) -> tuple[User, str]:

        normalized_email = email.strip().lower()
        user = self.user_repository.get_by_email(normalized_email)

        if user is None or not verify_password(
            password,
            user.password_hash,
        ):
            raise InvalidCredentialsError(
                "Incorrect email or password"
            )

        access_token = create_access_token(str(user.id))

        return user, access_token