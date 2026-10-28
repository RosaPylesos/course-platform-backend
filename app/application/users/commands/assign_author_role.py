from uuid import UUID

from app.application.exceptions import (
    ResourceNotFoundError,
    BusinessRuleError,
)
from app.application.unit_of_work import UnitOfWork

from app.models.enums import UserRole
from app.models.user import User



class AssignAuthorRoleCommand:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def execute(
        self, 
        user_id: UUID,
        current_user: User
        ) -> None:

        user = self.uow.users.get_by_id(user_id)

        if user is None:
            raise ResourceNotFoundError("User not found")

        if user.id == current_user.id:
            raise BusinessRuleError(
                "You cannot assign yourself as author while being an admin"
            )

        if user.role == UserRole.AUTHOR:
            return

        try:
            user.role = UserRole.AUTHOR
            self.uow.commit()
        except Exception:
            self.uow.rollback()
            raise