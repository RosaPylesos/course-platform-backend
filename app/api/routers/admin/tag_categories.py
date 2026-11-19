from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, status, Depends

from app.api.dependencies import Db_Session
from app.api.deps.tags import get_all_tag_categories_query
from app.api.schemas.tags import TagCategoryListParams
from app.api.mappers.tag_mapper import (
    to_tag_categories_list_response,
)

from app.application.tag_categories.queries import (
    GetAllTagCategoriesInput,
    GetAllTagCategoriesQuery,
)
from app.application.tag_categories.commands import (
    CreateTagCategoryCommand,
    UpdateTagCategoryCommand,
    DeleteTagCategoryCommand,
)

from app.infrastructure.unit_of_work import (
    SqlAlchemyUnitOfWork,
)

from app.models.tag_category import TagCategory

from app.schemas.tag_category import (
    TagCategoryListResponse,
    TagCategoryResponse,
    TagCategoryCreate,
    TagCategoryUpdate,
)

router = APIRouter(
    prefix="/tag-categories",
    tags=["Admin Tag Categories"],
)

@router.get(
    "/",
    response_model=TagCategoryListResponse,
    status_code=status.HTTP_200_OK,
)
def get_tag_categories(
    params: Annotated[TagCategoryListParams, Depends()],
    query: Annotated[
        GetAllTagCategoriesQuery,
        Depends(get_all_tag_categories_query)
    ],
) -> list[TagCategory]:

    input = GetAllTagCategoriesInput(
        **params.model_dump()
    )
    result = query.execute(input)
    return to_tag_categories_list_response(result)

@router.post(
    "/",
    response_model=TagCategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_tag_category(
    category_data: TagCategoryCreate,
    db: Db_Session,
) -> TagCategory:

    command = CreateTagCategoryCommand(
        SqlAlchemyUnitOfWork(db)
    )
    return command.execute(category_data)

@router.patch(
    "/{category_id}",
    response_model=TagCategoryResponse,
    status_code=status.HTTP_200_OK,
)
def update_tag_category(
    category_id: UUID,
    category_data: TagCategoryUpdate,
    db: Db_Session,
) -> TagCategory:

    command = UpdateTagCategoryCommand(
        SqlAlchemyUnitOfWork(db)
    )
    return command.execute(
        category_id,
        category_data,
    )

@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_tag_category(
    category_id: UUID,
    db: Db_Session,
) -> None:

    command = DeleteTagCategoryCommand(
        SqlAlchemyUnitOfWork(db)
    )
    command.execute(category_id)