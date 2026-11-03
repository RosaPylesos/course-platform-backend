from app.api.dependencies import Db_Session
from app.application.courses.queries import (
    GetCoursesQuery,
)
from app.application.courses.resolve_catalog_filters import (
    ResolveCatalogFilters,
)

from app.infrastructure.course_repository import SqlAlchemyCourseRepository
from app.infrastructure.topic_repository import SqlAlchemyTopicRepository
from app.infrastructure.tag_repository import SqlAlchemyTagRepository



def get_course_catalog_query(
    db: Db_Session,
) -> GetCoursesQuery:
    
    return GetCoursesQuery(
        SqlAlchemyCourseRepository(db),
        filter_resolver=ResolveCatalogFilters(
            topic_repo=SqlAlchemyTopicRepository(db),
            tag_repo=SqlAlchemyTagRepository(db),
        ),
    )