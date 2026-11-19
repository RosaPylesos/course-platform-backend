from typing import Annotated
from fastapi import Depends

from app.api.dependencies import (
    Db_Session,
    Unit_Of_Work_Dependency
)

from app.application.users.commands import (
    UpdateMyProfileCommand,
)
from app.application.users.queries import (
    GetMyProfileQuery,
    GetAllUsersQuery,
)

from app.infrastructure.user_repository import (
    SqlAlchemyUserRepository
)

def get_my_profile_query(
    db: Db_Session,
) -> GetMyProfileQuery:

    return GetMyProfileQuery(
        SqlAlchemyUserRepository(db),
    )

My_Profile_Query = Annotated[
    GetMyProfileQuery,
    Depends(get_my_profile_query),
]

def get_all_users_query(
    db: Db_Session,
) -> GetAllUsersQuery:

    return GetAllUsersQuery(
        SqlAlchemyUserRepository(db),
    )

All_Users_Query = Annotated[
    GetAllUsersQuery,
    Depends(get_all_users_query),
]

def get_update_my_profile_command(
    uow: Unit_Of_Work_Dependency,
) -> UpdateMyProfileCommand:

    return UpdateMyProfileCommand(uow)

Update_My_Profile_Command = Annotated[
    UpdateMyProfileCommand,
    Depends(get_update_my_profile_command),
]