from uuid import UUID
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db

from app.application.tag_categories.queries import (
    GetTagCategoryQuery,
    GetTagCategoriesQuery,
)

from app.infrastructure.tag_category_repository import (
    SqlAlchemyTagCategoryRepository,
)

from app.models.tag_category import TagCategory

from app.schemas.tag_category import(
    TagCategoryResponse,
    PublicTagCategoryResponse,
)

router = APIRouter(
    prefix="/tag-categories",
    tags=["Tag Categories"],
)

@router.get(
    "/",
    response_model=list[PublicTagCategoryResponse],
    status_code=status.HTTP_200_OK,
)
def get_tag_categories_with_tags(
    db: Annotated[Session, Depends(get_db)],
) -> list[TagCategory]:

    query = GetTagCategoriesQuery(
        SqlAlchemyTagCategoryRepository(db),
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