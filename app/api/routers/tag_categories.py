from uuid import UUID
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, require_roles

from app.application.tag_categories.queries import (
    GetTagCategoryQuery,
    GetTagCategoriesQuery,
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
)

router = APIRouter(
    prefix="/tag-categories",
    tags=["Tag Categories"],
)

@router.get(
    "/",
    response_model=list[TagCategoryResponse],
    status_code=status.HTTP_200_OK,
)
def get_tag_categories(
    db: Annotated[Session, Depends(get_db)],
) -> list[TagCategory]:

    query = GetTagCategoriesQuery(
        SqlAlchemyTagCategoryRepository(db)
    )
    return query.execute()

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