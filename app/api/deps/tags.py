from typing import Annotated

from sqlalchemy.orm import Session

from fastapi import Depends

from app.api.dependencies import get_db

from app.application.tags.queries import (
    GetTagsQuery,
)
from app.application.tag_categories.queries import (
    GetTagCategoriesQuery,
)

from app.infrastructure.tag_category_repository import (
    SqlAlchemyTagCategoryRepository,
)
from app.infrastructure.tag_repository import (
    SqlAlchemyTagRepository,
)

def get_tag_categories_query(
    db: Annotated[Session, Depends(get_db)],
) -> GetTagCategoriesQuery:

    return GetTagCategoriesQuery(
        SqlAlchemyTagCategoryRepository(db),
    )

def get_tags_query(
    db: Annotated[Session, Depends(get_db)],
) -> GetTagsQuery:

    return GetTagsQuery(
        SqlAlchemyTagRepository(db),
    )