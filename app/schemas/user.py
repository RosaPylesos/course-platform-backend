from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, EmailStr

from app.models.enums import UserRole

from app.schemas.user_topic import UserInterestResponse

class UserRegister(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=64,
    )
    surname: str | None = Field(
        default=None,
        max_length=64,
    )
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=128,
    )

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=128,
    )

class UserUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=64,
    )
    surname: str | None = Field(
        default=None,
        max_length=64,
    )

class UserResponse(BaseModel):
    id: UUID
    name: str
    surname: str | None
    email: EmailStr
    role: UserRole
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserListResponse(BaseModel):
    items: list[UserResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

class UserProfileResponse(BaseModel):
    id: UUID
    name: str
    surname: str | None
    email: EmailStr
    role: UserRole
    created_at: datetime
    topics: list[UserInterestResponse]

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"