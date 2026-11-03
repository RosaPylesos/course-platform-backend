from uuid import UUID

from fastapi import APIRouter, status

from app.api.dependencies import Db_Session

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
    db: Db_Session,
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
    db: Db_Session,
) -> TagCategory:

    query = GetTagCategoryQuery(
        SqlAlchemyTagCategoryRepository(db)
    )
    return query.execute(category_id)