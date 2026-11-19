from app.models.user import User

from app.schemas.user import (
    UserResponse,
    UserProfileResponse,
    UserListResponse,
)
from app.schemas.user_topic import UserInterestResponse

from app.application.users.views import AllUsersView



def to_user_profile_response(
    user: User,
) -> UserProfileResponse:

    return UserProfileResponse(
        id=user.id,
        name=user.name,
        surname=user.surname,
        email=user.email,
        role=user.role,
        created_at=user.created_at,
        topics=[
            UserInterestResponse.model_validate(user_topic.topic)
            for user_topic in user.user_topics
        ],
    )

def to_user_list_response(
    view: AllUsersView,
) -> UserListResponse:

    return UserListResponse(
        items=[
            UserResponse.model_validate(user)
            for user in view.items
        ],
        total=view.total,
        page=view.page,
        page_size=view.page_size,
        total_pages=view.total_pages,
    )