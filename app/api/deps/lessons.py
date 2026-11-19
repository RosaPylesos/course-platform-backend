from typing import Annotated

from sqlalchemy.orm import Session

from fastapi import Depends

from app.api.dependencies import Db_Session

from app.application.lessons.queries import (
    GetAllLessonsQuery,
)

from app.infrastructure.lesson_repository import (
    SqlAlchemyLessonRepository,
)

def get_all_lessons_query(
    db: Db_Session,
) -> GetAllLessonsQuery:

    return GetAllLessonsQuery(
        SqlAlchemyLessonRepository(db),
)