from typing import Annotated
from fastapi import APIRouter, status, Depends

from app.api.deps.lessons import get_all_lessons_query
from app.api.schemas.lesson_list import ManagedLessonListParams
from app.api.mappers.lesson_mapper import (
    to_managed_lesson_list_response,
)

from app.application.lessons.queries import (
    GetAllLessonsQuery,
    GetAllLessonsInput,
)

from app.schemas.lesson import ManagedLessonListResponse

router = APIRouter(
    prefix="/lessons",
    tags=["Admin Lessons"],
)

@router.get(
    "/",
    response_model=ManagedLessonListResponse,
    status_code=status.HTTP_200_OK,
)
def get_all_lessons(
    query: Annotated[
        GetAllLessonsQuery,
        Depends(get_all_lessons_query),
    ],
    params: Annotated[
        ManagedLessonListParams,
        Depends(),
    ],
) -> ManagedLessonListResponse:

    input = GetAllLessonsInput(**params.model_dump())
    result = query.execute(input)

    return to_managed_lesson_list_response(result)