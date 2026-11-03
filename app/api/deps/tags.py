from app.api.dependencies import Db_Session

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
    db: Db_Session,
) -> GetAllTagCategoriesQuery:

    return GetAllTagCategoriesQuery(
        SqlAlchemyTagCategoryRepository(db),
    )

def get_all_tags_query(
    db: Db_Session,
) -> GetAllTagsQuery:

    return GetAllTagsQuery(
        SqlAlchemyTagRepository(db),
    )