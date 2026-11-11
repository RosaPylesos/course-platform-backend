from uuid import UUID

from fastapi import APIRouter, status

from app.api.dependencies import Db_Session, Current_User

from app.application.user_topics.queries import (
    GetUserTopicsQuery,
)
from app.application.user_topics.commands import (
    AddUserTopicCommand,
    RemoveUserTopicCommand,
    UpdateUserTopicsCommand,
)

from app.infrastructure.user_topic_repository import (
    SqlAlchemyUserTopicRepository,
)
from app.infrastructure.unit_of_work import (
    SqlAlchemyUnitOfWork,
)

from app.models.topic import Topic

from app.schemas.user_topic import (
    UserTopicCreate,
    UserInterestResponse,
    UserTopicsUpdate,
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
    current_user: Current_User,
    db: Db_Session,
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
    current_user: Current_User,
    db: Db_Session,
) -> None:

    command = AddUserTopicCommand(
        SqlAlchemyUnitOfWork(db)
    )
    command.execute(
        user_id=current_user.id,
        topic_id=topic_data.topic_id,
    )

@router.put(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
def update_user_topics(
    topic_data: UserTopicsUpdate,
    current_user: Current_User,
    db: Db_Session,
) -> None:

    command = UpdateUserTopicsCommand(
        SqlAlchemyUnitOfWork(db),
    )
    command.execute(
        user_id=current_user.id,
        topic_ids=topic_data.topic_ids,
    )

@router.delete(
    "/{topic_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_user_topic(
    topic_id: UUID,
    current_user: Current_User,
    db: Db_Session,
) -> None:

    command = RemoveUserTopicCommand(
        SqlAlchemyUnitOfWork(db)
    )
    command.execute(
        user_id=current_user.id,
        topic_id=topic_id,
    )