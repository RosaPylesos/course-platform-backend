from app.api.dependencies import Db_Session

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

def get_all_users_query(
    db: Db_Session,
) -> GetAllUsersQuery:

    return GetAllUsersQuery(
        SqlAlchemyUserRepository(db),
    )