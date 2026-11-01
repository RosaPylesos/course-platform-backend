from typing import Annotated

from sqlalchemy.orm import Session

from fastapi import Depends

from app.api.dependencies import get_db

from app.application.courses.queries import (
    GetMyCourseQuery,
    GetMyCoursesQuery,
    GetCoursesQuery,
    GetAllCoursesQuery,
)
from app.application.courses.resolve_catalog_filters import (
    ResolveCatalogFilters,
)

from app.infrastructure.course_repository import (
    SqlAlchemyCourseRepository,
)
from app.infrastructure.topic_repository import (
    SqlAlchemyTopicRepository,
)
from app.infrastructure.tag_repository import (
    SqlAlchemyTagRepository,
)

def get_my_course_query(
    db: Annotated[Session, Depends(get_db)],
) -> GetMyCourseQuery:

    return GetMyCourseQuery(
        SqlAlchemyCourseRepository(db),
    )

def get_my_courses_query(
    db: Annotated[Session, Depends(get_db)],
) -> GetMyCoursesQuery:

    return GetMyCoursesQuery(
        SqlAlchemyCourseRepository(db),
    )

def get_course_catalog_query(
    db: Annotated[Session, Depends(get_db)],
) -> GetCoursesQuery:
    
    return GetCoursesQuery(
        SqlAlchemyCourseRepository(db),
        filter_resolver=ResolveCatalogFilters(
            topic_repo=SqlAlchemyTopicRepository(db),
            tag_repo=SqlAlchemyTagRepository(db),
        ),
    )

def get_all_courses_query(
    db: Annotated[Session, Depends(get_db)],
) -> GetAllCoursesQuery:

    return GetAllCoursesQuery(
        SqlAlchemyCourseRepository(db),
    )