from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db

from app.application.courses.queries import (
    GetHomePageQuery,
)

from app.infrastructure.course_repository import (
    SqlAlchemyCourseRepository,
)
from app.infrastructure.user_topic_repository import (
    SqlAlchemyUserTopicRepository,
)

def get_home_page_query(
    db: Annotated[Session, Depends(get_db)],
) -> GetHomePageQuery:
    
    return GetHomePageQuery(
        course_repository=SqlAlchemyCourseRepository(db),
        user_topic_repository=SqlAlchemyUserTopicRepository(db),
    )