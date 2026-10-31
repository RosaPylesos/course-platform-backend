from uuid import UUID
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps.tags import (
    get_tag_categories_query,
)
from app.api.schemas.tags import TagCategoryListParams
from app.api.dependencies import get_db, require_roles
from app.api.mappers.tag_mapper import (
    to_tag_categories_list_response,
)

from app.application.tag_categories.queries import (
    GetTagCategoryQuery,
    GetTagCategoriesQuery,
    GetTagCategoriesInput,
)
from app.application.tag_categories.commands import (
    CreateTagCategoryCommand,
    UpdateTagCategoryCommand,
    DeleteTagCategoryCommand,
)

from app.infrastructure.tag_category_repository import (
    SqlAlchemyTagCategoryRepository,
)
from app.infrastructure.unit_of_work import (
    SqlAlchemyUnitOfWork,
)

from app.models.tag_category import TagCategory
from app.models.user import User
from app.models.enums import UserRole

from app.schemas.tag_category import(
    TagCategoryCreate,
    TagCategoryUpdate,
    TagCategoryResponse,
    TagCategoryListResponse,
)

router = APIRouter(
    prefix="/tag-categories",
    tags=["Tag Categories"],
)

@router.get(
    "/",
    response_model=TagCategoryListResponse,
    status_code=status.HTTP_200_OK,
)
def get_tag_categories(
    params: Annotated[TagCategoryListParams, Depends()],
    query: Annotated[
        GetTagCategoriesQuery,
        Depends(get_tag_categories_query)
    ],
) -> list[TagCategory]:

    input = GetTagCategoriesInput(
        **params.model_dump()
    )
    items, total = query.execute(input)
    return to_tag_categories_list_response(
        items, total, params.page, params.page_size,
    )

@router.get(
    "/{category_id}",
    response_model=TagCategoryResponse,
    status_code=status.HTTP_200_OK,
)
def get_tag_category(
    category_id: UUID,
    db: Annotated[Session, Depends(get_db)],
) -> TagCategory:

    query = GetTagCategoryQuery(
        SqlAlchemyTagCategoryRepository(db)
    )
    return query.execute(category_id)

@router.post(
    "/",
    response_model=TagCategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_tag_category(
    category_data: TagCategoryCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[
        User,
        Depends(require_roles(UserRole.ADMIN))
    ],
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
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[
        User,
        Depends(require_roles(UserRole.ADMIN)),
    ],
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
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[
        User,
        Depends(require_roles(UserRole.ADMIN)),
    ],
) -> None:

    command = DeleteTagCategoryCommand(
        SqlAlchemyUnitOfWork(db)
    )
    command.execute(category_id)