from uuid import UUID

from fastapi import APIRouter, status

from app.api.dependencies import Db_Session

from app.application.tags.queries import (
    GetTagQuery,
)

from app.infrastructure.tag_repository import (
    SqlAlchemyTagRepository,
)

from app.models.tag import Tag

from app.schemas.tag import (
    TagResponse,
)

router = APIRouter(
    prefix="/tags",
    tags=["Tags"],
)

@router.get(
    "/{tag_id}",
    response_model=TagResponse,
    status_code=status.HTTP_200_OK,
)
def get_tag(
    tag_id: UUID,
    db: Db_Session,
) -> Tag:

    query = GetTagQuery(
        SqlAlchemyTagRepository(db)
    )
    return query.execute(tag_id)