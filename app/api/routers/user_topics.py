from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_user

from app.application.user_topics.queries import (
    GetUserTopicsQuery,
)
from app.application.user_topics.commands import (
    AddUserTopicCommand,
    RemoveUserTopicCommand,
)

from app.infrastructure.user_topic_repository import (
    SqlAlchemyUserTopicRepository,
)
from app.infrastructure.unit_of_work import (
    SqlAlchemyUnitOfWork,
)

from app.models.topic import Topic
from app.models.user import User

from app.schemas.user_topic import (
    UserTopicCreate,
    UserInterestResponse,
)

router = APIRouter(
    prefix="/users/me/topics",
    tags=["User Topics"],
)

@router.get(
    "/",
    response_model=list[UserInterestResponse],
    status_code=status.HTTP_200_OK,
)
def get_user_topics(
    current_user: Annotated[
        User, 
        Depends(get_current_user)
    ],
    db: Annotated[Session, Depends(get_db)],
) -> list[Topic]:

    query = GetUserTopicsQuery(
        SqlAlchemyUserTopicRepository(db)
    )
    return query.execute(current_user.id)

@router.post(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def add_user_topic(
    topic_data: UserTopicCreate,
    current_user: Annotated[
        User, 
        Depends(get_current_user)
    ],
    db: Annotated[Session, Depends(get_db)],
) -> None:

    command = AddUserTopicCommand(
        SqlAlchemyUnitOfWork(db)
    )
    command.execute(
        user_id=current_user.id,
        topic_id=topic_data.topic_id,
    )

@router.delete(
    "/{topic_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_user_topic(
    topic_id: UUID,
    current_user: Annotated[
        User, 
        Depends(get_current_user)
    ],
    db: Annotated[Session, Depends(get_db)],
) -> None:

    command = RemoveUserTopicCommand(
        SqlAlchemyUnitOfWork(db)
    )
    command.execute(
        user_id=current_user.id,
        topic_id=topic_id,
    )