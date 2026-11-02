from uuid import UUID
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db

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
    db: Annotated[Session, Depends(get_db)],
) -> Tag:

    query = GetTagQuery(
        SqlAlchemyTagRepository(db)
    )
    return query.execute(tag_id)