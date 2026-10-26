from uuid import UUID

from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, require_roles

from app.application.topics.queries import (
    GetTopicsQuery,
    GetTopicQuery,
)
from app.application.topics.commands import (
    CreateTopicCommand,
    UpdateTopicCommand,
    DeleteTopicCommand,
)

from app.infrastructure.topic_repository import (
    SqlAlchemyTopicRepository,
)
from app.infrastructure.unit_of_work import (
    SqlAlchemyUnitOfWork,
)

from app.models.topic import Topic
from app.models.user import User
from app.models.enums import UserRole

from app.schemas.topic import (
    TopicCreate, 
    TopicResponse, 
    TopicUpdate,
)

router = APIRouter(
    prefix="/topics",
    tags=["Topics"],
)

@router.get(
    "/", 
    response_model=list[TopicResponse],
    status_code=status.HTTP_200_OK,
)
def get_topics(
    db: Annotated[Session, Depends(get_db)],
) -> list[Topic]:
    
    query = GetTopicsQuery(
        SqlAlchemyTopicRepository(db)
    )
    return query.execute()

@router.get(
    "/{topic_id}", 
    response_model=TopicResponse,
    status_code=status.HTTP_200_OK,
)
def get_topic(
    topic_id: UUID,
    db: Annotated[Session, Depends(get_db)],
) -> Topic:
    
    query = GetTopicQuery(
        SqlAlchemyTopicRepository(db)
    )
    return query.execute(topic_id)

@router.post(
    "/", 
    response_model=TopicResponse, 
    status_code=status.HTTP_201_CREATED,
)
def create_topic(
    topic_data: TopicCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[
        User,
        Depends(require_roles(UserRole.ADMIN)),
    ],
) -> Topic:

    command = CreateTopicCommand(
        SqlAlchemyUnitOfWork(db)
    )
    return command.execute(topic_data)

@router.patch(
    "/{topic_id}", 
    response_model=TopicResponse,
    status_code=status.HTTP_200_OK,
)
def update_topic(
    topic_id: UUID,
    topic_data: TopicUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[
        User,
        Depends(require_roles(UserRole.ADMIN)),
    ],
) -> Topic:

    command = UpdateTopicCommand(
        SqlAlchemyUnitOfWork(db)
    )
    return command.execute(
        topic_id,
        topic_data,
    )

@router.delete(
    "/{topic_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_topic(
    topic_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[
        User,
        Depends(require_roles(UserRole.ADMIN)),
    ],
) -> None:
    
    command = DeleteTopicCommand(
        SqlAlchemyUnitOfWork(db)
    )
    command.execute(topic_id)