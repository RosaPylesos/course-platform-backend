from app.models.user import User

from app.schemas.user import UserProfileResponse
from app.schemas.user_topic import UserInterestResponse



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