from uuid import UUID

from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db

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
    db: Annotated[Session, Depends(get_db)],
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
    db: Annotated[Session, Depends(get_db)],
) -> Topic:
    
    query = GetTopicQuery(
        SqlAlchemyTopicRepository(db)
    )
    return query.execute(topic_id)