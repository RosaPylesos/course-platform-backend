import uuid
import jwt

from collections.abc import Generator
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import (
    OAuth2PasswordBearer, 
    OAuth2PasswordRequestForm,
)

from jwt.exceptions import InvalidTokenError

from sqlalchemy.orm import Session

from app.database.connection import SessionLocal, settings

from app.infrastructure.user_repository import (
    SqlAlchemyUserRepository
)

from app.models.user import User
from app.models.enums import UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")

optional_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/users/token",
    auto_error=False,
)

OAuth2_Form = Annotated[OAuth2PasswordRequestForm, Depends()]

# DB Dependency

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

Db_Session = Annotated[Session, Depends(get_db)]

# Get user for further actions with API

def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Db_Session,
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )

        subject = payload.get("sub")
        if not isinstance(subject, str):
            raise credentials_exception

        user_id = uuid.UUID(subject)

    except (InvalidTokenError, ValueError):
        raise credentials_exception from None

    user_repository = SqlAlchemyUserRepository(db)
    user = user_repository.get_by_id(user_id)

    if user is None:
        raise credentials_exception

    return user

Current_User = Annotated[User, Depends(get_current_user)]

# Get optional user for further actions with API

def get_optional_current_user(
    token: Annotated[str, Depends(optional_oauth2_scheme)],
    db: Db_Session,
) -> User | None:

    if token is None:
        return None

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )

        subject = payload.get("sub")
        if not isinstance(subject, str):
            return None

        user_id = uuid.UUID(subject)
    except (InvalidTokenError, ValueError):
        return None

    user_repository = SqlAlchemyUserRepository(db)
    user = user_repository.get_by_id(user_id)
    
    return user

Optional_Current_User = Annotated[
    User | None, 
    Depends(get_optional_current_user),
]

# User's Role check

def require_roles(*allowed_roles: UserRole):
    def role_checker(
            current_user: User = Depends(get_current_user),
    ) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to perform this action",
            )

        return current_user

    return role_checker

Author_Or_Admin_User = Annotated[
    User,
    Depends(require_roles(
        UserRole.AUTHOR,
        UserRole.ADMIN,
    )),
]

Admin_User = Annotated[
    User,
    Depends(require_roles(UserRole.ADMIN)),
]