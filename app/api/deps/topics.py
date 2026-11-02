from typing import Annotated

from sqlalchemy.orm import Session

from fastapi import Depends

from app.api.dependencies import get_db

from app.application.topics.queries import (
    GetAllTopicsQuery,
)

from app.infrastructure.topic_repository import (
    SqlAlchemyTopicRepository,
)

def get_all_topics_query(
    db: Annotated[Session, Depends(get_db)],
) -> GetAllTopicsQuery:

    return GetAllTopicsQuery(
        SqlAlchemyTopicRepository(db),
    )