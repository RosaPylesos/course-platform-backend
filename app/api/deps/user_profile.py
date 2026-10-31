from typing import Annotated

from sqlalchemy.orm import Session

from fastapi import Depends

from app.api.dependencies import get_db

from app.application.users.queries import (
    GetMyProfileQuery,
)

from app.infrastructure.user_repository import (
    SqlAlchemyUserRepository
)

def get_my_profile_query(
    db: Annotated[Session, Depends(get_db)],
) -> GetMyProfileQuery:

    return GetMyProfileQuery(
        SqlAlchemyUserRepository(db),
    )