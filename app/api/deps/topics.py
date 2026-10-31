from typing import Annotated

from sqlalchemy.orm import Session

from fastapi import Depends

from app.api.dependencies import get_db

from app.application.topics.queries import (
    GetTopicsQuery,
)

from app.infrastructure.topic_repository import (
    SqlAlchemyTopicRepository,
)

def get_topics_query(
    db: Annotated[Session, Depends(get_db)],
) -> GetTopicsQuery:

    return GetTopicsQuery(
        SqlAlchemyTopicRepository(db),
    )