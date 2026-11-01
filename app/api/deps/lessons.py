from typing import Annotated

from sqlalchemy.orm import Session

from fastapi import Depends

from app.api.dependencies import get_db

from app.application.lessons.queries import (
    GetAllLessonsQuery,
)

from app.infrastructure.lesson_repository import (
    SqlAlchemyLessonRepository,
)

def get_all_lessons_query(
    db: Annotated[Session, Depends(get_db)],
) -> GetAllLessonsQuery:

    return GetAllLessonsQuery(
        SqlAlchemyLessonRepository(db),
)