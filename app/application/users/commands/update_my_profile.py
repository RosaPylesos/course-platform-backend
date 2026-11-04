from uuid import UUID

from app.application.exceptions import (
    ResourceNotFoundError,
    InvalidInputError,
)
from app.application.unit_of_work import UnitOfWork

from app.models.user import User

from app.schemas.user import UserUpdate



class UpdateMyProfileCommand:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def execute(
        self,
        user_id: UUID,
        user_data: UserUpdate,
    ) -> User:

        user = self.uow.users.get_by_id(user_id)

        if user is None:
            raise ResourceNotFoundError(
                "User not found"
            )

        update_data = user_data.model_dump(exclude_unset=True)

        if not update_data:
            raise InvalidInputError("No fields to update")

        if (
            "name" in update_data
            and update_data["name"] is None
        ):
            raise InvalidInputError("Name cannot be null")

        try:
            for field, value in update_data.items():
                setattr(user, field, value)

            self.uow.commit()
            self.uow.refresh(user)

        except Exception:
            self.uow.rollback()
            raise

        return user