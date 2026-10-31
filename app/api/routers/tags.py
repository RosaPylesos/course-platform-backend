from uuid import UUID
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.schemas.tags import TagListParams
from app.api.dependencies import get_db, require_roles
from app.api.mappers.tag_mapper import (
    to_tag_list_response,
)
from app.api.deps.tags import get_tags_query

from app.application.tags.queries import (
    GetTagQuery,
    GetTagsQuery,
    GetTagsInput,
)
from app.application.tags.commands import (
    CreateTagCommand,
    UpdateTagCommand,
    DeleteTagCommand,
)

from app.infrastructure.tag_repository import (
    SqlAlchemyTagRepository,
)
from app.infrastructure.unit_of_work import(
    SqlAlchemyUnitOfWork,
)

from app.models.tag import Tag
from app.models.user import User
from app.models.enums import UserRole

from app.schemas.tag import (
    TagCreate,
    TagUpdate,
    TagResponse,
    TagListResponse,
)

router = APIRouter(
    prefix="/tags",
    tags=["Tags"],
)

@router.get(
    "/",
    response_model=TagListResponse,
    status_code=status.HTTP_200_OK,
)
def get_tags(
    query: Annotated[
        GetTagsQuery,
        Depends(get_tags_query),
    ],
    params: Annotated[
        TagListParams,
        Depends(),
    ],
) -> TagListResponse:

    input = GetTagsInput(**params.model_dump())
    items, total = query.execute(input)
    return to_tag_list_response(
        items, total, params.page, params.page_size,
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

@router.post(
    "/",
    response_model=TagResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_tag(
    tag_data: TagCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[
        User,
        Depends(require_roles(UserRole.ADMIN)),
    ],
) -> Tag:

    command = CreateTagCommand(
        SqlAlchemyUnitOfWork(db)
    )
    return command.execute(tag_data)

@router.patch(
    "/{tag_id}",
    response_model=TagResponse,
    status_code=status.HTTP_200_OK,
)
def update_tag(
    tag_id: UUID,
    tag_data: TagUpdate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[
        User,
        Depends(require_roles(UserRole.ADMIN)),
    ],
) -> Tag:

    command = UpdateTagCommand(
        SqlAlchemyUnitOfWork(db)
    )
    return command.execute(tag_id, tag_data)

@router.delete(
    "/{tag_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_tag(
    tag_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[
        User,
        Depends(require_roles(UserRole.ADMIN)),
    ],
) -> None:

    command = DeleteTagCommand(
        SqlAlchemyUnitOfWork(db)
    )
    command.execute(tag_id)