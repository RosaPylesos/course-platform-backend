from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, status, Depends

from app.api.dependencies import Db_Session
from app.api.deps.topics import get_all_topics_query
from app.api.schemas.topics import TopicListParams
from app.api.mappers.topic_mapper import (
    to_topics_list_response,
)

from app.application.topics.queries import (
    GetAllTopicsQuery,
    GetAllTopicsInput,
)
from app.application.topics.commands import (
    CreateTopicCommand,
    UpdateTopicCommand,
    DeleteTopicCommand,
)

from app.infrastructure.unit_of_work import (
    SqlAlchemyUnitOfWork,
)

from app.models.topic import Topic

from app.schemas.topic import (
    TopicListResponse,
    TopicResponse,
    TopicCreate,
    TopicUpdate,
)

router = APIRouter(
    prefix="/topics",
    tags=["Admin Topics"]
)

@router.get(
    "/", 
    response_model=TopicListResponse,
    status_code=status.HTTP_200_OK,
)
def get_all_topics(
    query: Annotated[
        GetAllTopicsQuery,
        Depends(get_all_topics_query),
    ],
    params: Annotated[
        TopicListParams,
        Depends(),
    ]
) -> TopicListResponse:
    
    input = GetAllTopicsInput(
        **params.model_dump()
    )
    result = query.execute(input)
    
    return to_topics_list_response(result)

@router.post(
    "/", 
    response_model=TopicResponse, 
    status_code=status.HTTP_201_CREATED,
)
def create_topic(
    topic_data: TopicCreate,
    db: Db_Session,
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
    db: Db_Session,
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
    db: Db_Session,
) -> None:
    
    command = DeleteTopicCommand(
        SqlAlchemyUnitOfWork(db)
    )
    command.execute(topic_id)