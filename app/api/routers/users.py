from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_user

from app.application.users.queries import (
    AuthenticateUserQuery,
)
from app.application.users.commands import (
    RegisterUserCommand,
)

from app.infrastructure.user_repository import(
    SqlAlchemyUserRepository,
)
from app.infrastructure.unit_of_work import (
    SqlAlchemyUnitOfWork,
)

from app.models.user import User
from app.schemas.user import (
    UserRegister, 
    UserResponse,
    UserLogin,
    TokenResponse,
)

router = APIRouter(
    prefix="/users", 
    tags=["Users"],
)

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user_data: UserRegister,
    db: Annotated[Session, Depends(get_db)],
) -> User:
    
    command = RegisterUserCommand(
        SqlAlchemyUnitOfWork(db)
    )
    return command.execute(user_data)

@router.post(
    "/login", 
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
def login_user(
    user_data: UserLogin,
    db: Annotated[Session, Depends(get_db)],
) -> TokenResponse:
    
    query = AuthenticateUserQuery(
        SqlAlchemyUserRepository(db)
    )
    _, access_token = query.execute(
        email=str(user_data.email),
        password=user_data.password,
    )
    return TokenResponse(access_token=access_token)

@router.post(
    "/token", 
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
def login_for_swagger(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
) -> TokenResponse:
    
    query = AuthenticateUserQuery(
            SqlAlchemyUserRepository(db)
        )
    _, access_token = query.execute(
        email=form_data.username,
        password=form_data.password,
    )
    return TokenResponse(access_token=access_token)

@router.get(
    "/me", 
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def get_me(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    return current_user