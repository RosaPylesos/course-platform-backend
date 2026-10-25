from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_user
from app.core.security import (
    create_access_token, 
    hash_password,
    verify_password,
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
    
    email = str(user_data.email).strip().lower()

    existing_user = db.scalar(
        select(User).where(
            User.email == email
        )
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )

    user = User(
        name = user_data.name,
        surname = user_data.surname,
        email = email,
        password_hash = hash_password(user_data.password),
    )

    db.add(user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )

    db.refresh(user)

    return user



@router.post(
    "/login", 
    response_model=TokenResponse,
    #status_code=status.HTTP_200_OK,
)
def login_user(
    user_data: UserLogin,
    db: Annotated[Session, Depends(get_db)],
) -> TokenResponse:
    
    email = str(user_data.email).strip().lower()

    user = db.scalar(
        select(User).where(User.email == email)
    )

    if user is None or not verify_password(
        user_data.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(str(user.id))

    return TokenResponse(access_token=access_token)



@router.post(
    "/token", 
    response_model=TokenResponse,
    #status_code=status.HTTP_200_OK,
)
def login_for_swagger(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    #form_data: OAuth2PasswordRequestForm = Depends(),
    db: Annotated[Session, Depends(get_db)],
) -> TokenResponse:
    
    email = form_data.username.strip().lower()

    user = db.scalar(
        select(User).where(User.email == email)
    )

    if user is None or not verify_password(
        form_data.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(str(user.id))

    return TokenResponse(access_token=access_token)

@router.get(
    "/me", 
    response_model=UserResponse,
    #status_code=status.HTTP_200_OK,
)
def get_me(
    current_user: Annotated[User, Depends(get_current_user)],
    #current_user: User = Depends(get_current_user),
) -> User:
    return current_user