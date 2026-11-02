from typing import Annotated

from sqlalchemy.orm import Session

from fastapi import Depends

from app.api.dependencies import get_db

from app.application.tags.queries import (
    GetAllTagsQuery,
)
from app.application.tag_categories.queries import (
    GetAllTagCategoriesQuery,
)

from app.infrastructure.tag_category_repository import (
    SqlAlchemyTagCategoryRepository,
)
from app.infrastructure.tag_repository import (
    SqlAlchemyTagRepository,
)

def get_all_tag_categories_query(
    db: Annotated[Session, Depends(get_db)],
) -> GetAllTagCategoriesQuery:

    return GetAllTagCategoriesQuery(
        SqlAlchemyTagCategoryRepository(db),
    )

def get_all_tags_query(
    db: Annotated[Session, Depends(get_db)],
) -> GetAllTagsQuery:

    return GetAllTagsQuery(
        SqlAlchemyTagRepository(db),
    )