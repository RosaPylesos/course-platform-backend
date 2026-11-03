from typing import Annotated
from fastapi import APIRouter, status, Depends

from app.api.schemas.manage_course import ManagedCourseListParams
from app.api.deps.courses import (
    get_all_courses_query,
)
from app.api.mappers.course_mapper import (
    to_managed_course_list_response,
)

from app.application.courses.queries import (
    GetAllCoursesInput,
    GetAllCoursesQuery,
)

from app.schemas.course import ManagedCourseListResponse

router = APIRouter(
    prefix="/courses",
    tags=["Admin Courses"],
)

@router.get(
    "/",
    response_model=ManagedCourseListResponse,
    status_code=status.HTTP_200_OK,
)
def get_all_courses(
    query: Annotated[
        GetAllCoursesQuery,
        Depends(get_all_courses_query),
    ],
    params: Annotated[
        ManagedCourseListParams,
        Depends(),
    ],
) -> ManagedCourseListResponse:

    input = GetAllCoursesInput(**params.model_dump())
    result = query.execute(input)
    return to_managed_course_list_response(
        result
    )