from typing import Annotated

from fastapi import Depends, APIRouter, status

from app.api.dependencies import get_optional_current_user
from app.api.deps.home_page import get_home_page_query
from app.api.mappers.course_mapper import (
    to_home_page_response,
)

from app.application.courses.queries import (
    GetHomePageQuery,
)

from app.models.user import User

from app.schemas.home_page import HomePageResponse

router = APIRouter(
    prefix="/home",
    tags=["Home"],
)

@router.get(
    "/",
    response_model=HomePageResponse,
    status_code=status.HTTP_200_OK,
)
def get_home_page(
    query: Annotated[
        GetHomePageQuery, 
        Depends(get_home_page_query)
    ],
    current_user: Annotated[
        User | None, 
        Depends(get_optional_current_user)
    ],
) -> HomePageResponse:

    sections = query.execute(
        user_id=current_user.id if current_user else None
    )

    return to_home_page_response(sections)