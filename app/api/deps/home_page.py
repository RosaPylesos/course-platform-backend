from app.api.dependencies import Db_Session

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
    db: Db_Session,
) -> GetHomePageQuery:
    
    return GetHomePageQuery(
        course_repository=SqlAlchemyCourseRepository(db),
        user_topic_repository=SqlAlchemyUserTopicRepository(db),
    )