from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.mappers.user_mapper import (
    to_user_profile_response,
)
from app.api.dependencies import (
    Current_User, 
    Db_Session,
    OAuth2_Form,
)
from app.api.deps.users import (
    get_my_profile_query,
    Update_My_Profile_Command,
)

from app.application.users.queries import (
    AuthenticateUserQuery,
    GetMyProfileQuery,
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
    UserProfileResponse,
    UserLogin,
    UserUpdate,
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
    db: Db_Session,
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
    db: Db_Session,
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
    form_data: OAuth2_Form,
    db: Db_Session,
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
    response_model=UserProfileResponse,
    status_code=status.HTTP_200_OK,
)
def get_me(
    current_user: Current_User,
    query: Annotated[
        GetMyProfileQuery, Depends(get_my_profile_query)
    ],
) -> UserProfileResponse:

    user = query.execute(current_user.id)
    return to_user_profile_response(user)

@router.patch(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
def update_my_profile(
    user_data: UserUpdate,
    current_user: Current_User,
    command: Update_My_Profile_Command,
) -> User:

    return command.execute(
        user_id=current_user.id,
        user_data=user_data,
    )