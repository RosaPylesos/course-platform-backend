from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import require_roles, get_db
from app.api.deps.users import get_all_users_query
from app.api.schemas.user_list import UserListParams

from app.api.mappers.user_mapper import (
    to_user_list_response,
)

from app.application.users.queries import (
    GetAllUsersInput,
    GetAllUsersQuery,
)
from app.application.users.commands import (
    AssignAuthorRoleCommand,
)

from app.infrastructure.unit_of_work import (
    SqlAlchemyUnitOfWork,
)

from app.models.user import User
from app.models.enums import UserRole

from app.schemas.user import UserListResponse

router = APIRouter(
    prefix="/users",
    tags=["Admin Users"],
)

@router.get(
    "/",
    response_model=UserListResponse,
    status_code=status.HTTP_200_OK,
)
def get_all_users(
    current_user: Annotated[
        User,
        Depends(require_roles(UserRole.ADMIN)),
    ],
    query: Annotated[
        GetAllUsersQuery, 
        Depends(get_all_users_query),
    ],
    params: Annotated[
        UserListParams, 
        Depends(),
    ],
) -> UserListResponse:

    input = GetAllUsersInput(**params.model_dump())
    result = query.execute(input)
    return to_user_list_response(result)

@router.patch(
    "/{user_id}/role",
    status_code=status.HTTP_204_NO_CONTENT,
)
def assign_author_role(
    user_id: UUID,
    current_user: Annotated[
        User,
        Depends(require_roles(UserRole.ADMIN)),
    ],
    db: Annotated[Session, Depends(get_db)],
) -> None:

    command = AssignAuthorRoleCommand(
        SqlAlchemyUnitOfWork(db)
    )
    command.execute(
        user_id=user_id,
        current_user=current_user,
    )