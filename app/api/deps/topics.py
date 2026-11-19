from app.api.dependencies import Db_Session

from app.application.topics.queries import (
    GetAllTopicsQuery,
)

from app.infrastructure.topic_repository import (
    SqlAlchemyTopicRepository,
)

def get_all_topics_query(
    db: Db_Session,
) -> GetAllTopicsQuery:

    return GetAllTopicsQuery(
        SqlAlchemyTopicRepository(db),
    )