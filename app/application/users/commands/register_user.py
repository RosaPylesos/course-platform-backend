from sqlalchemy.exc import IntegrityError

from app.application.exceptions import (
    ConflictError,
    DuplicateEmailError,
)
from app.application.unit_of_work import UnitOfWork

from app.core.security import hash_password

from app.models.user import User

from app.schemas.user import UserRegister



class RegisterUserCommand:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def execute(
        self,
        user_data: UserRegister,
    ) -> User:

        email = str(user_data.email).strip().lower()

        existing_user = self.uow.users.get_by_email(email)

        if existing_user is not None:
            raise ConflictError("User with this email already exists")

        user = User(
            name = user_data.name,
            surname = user_data.surname,
            email = email,
            password_hash = hash_password(user_data.password),
        )

        self.uow.users.add(user)

        try:
            self.uow.commit()
        except IntegrityError as exc:
            self.uow.rollback()

            if self.uow.users.get_by_email(email) is not None:
                raise DuplicateEmailError(
                    "User with this email already exists"
                ) from exc

            raise
        except Exception:
            self.uow.rollback()
            raise

        self.uow.refresh(user)

        return user