from uuid import UUID

from fastapi import APIRouter, status

from app.api.dependencies import Db_Session

from app.application.topics.queries import (
    GetTopicsQuery,
    GetTopicQuery,
)

from app.infrastructure.topic_repository import (
    SqlAlchemyTopicRepository,
)

from app.models.topic import Topic

from app.schemas.topic import (
    TopicResponse, 
    PublicTopicResponse,
)

router = APIRouter(
    prefix="/topics",
    tags=["Topics"],
)

@router.get(
    "/", 
    response_model=list[PublicTopicResponse],
    status_code=status.HTTP_200_OK,
)
def get_topics(
    db: Db_Session,
) -> list[Topic]:
    
    query = GetTopicsQuery(
        SqlAlchemyTopicRepository(db),
    )
    return query.execute()

@router.get(
    "/{topic_id}", 
    response_model=TopicResponse,
    status_code=status.HTTP_200_OK,
)
def get_topic(
    topic_id: UUID,
    db: Db_Session,
) -> Topic:
    
    query = GetTopicQuery(
        SqlAlchemyTopicRepository(db)
    )
    return query.execute(topic_id)