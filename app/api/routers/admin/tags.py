from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, status, Depends

from app.api.dependencies import Db_Session
from app.api.deps.tags import get_all_tags_query
from app.api.schemas.tags import TagListParams
from app.api.mappers.tag_mapper import (
    to_tag_list_response,
)

from app.application.tags.queries import (
    GetAllTagsInput,
    GetAllTagsQuery,
)
from app.application.tags.commands import (
    CreateTagCommand,
    UpdateTagCommand,
    DeleteTagCommand,
)

from app.infrastructure.unit_of_work import (
    SqlAlchemyUnitOfWork,
)

from app.models.tag import Tag

from app.schemas.tag import (
    TagListResponse, 
    TagResponse,
    TagCreate,
    TagUpdate,
)

router = APIRouter(
    prefix="/tags",
    tags=["Admin Tags"],
)

@router.get(
    "/",
    response_model=TagListResponse,
    status_code=status.HTTP_200_OK,
)
def get_all_tags(
    query: Annotated[
        GetAllTagsQuery,
        Depends(get_all_tags_query),
    ],
    params: Annotated[
        TagListParams,
        Depends(),
    ],
) -> TagListResponse:

    input = GetAllTagsInput(**params.model_dump())
    result = query.execute(input)
    return to_tag_list_response(result)

@router.post(
    "/",
    response_model=TagResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_tag(
    tag_data: TagCreate,
    db: Db_Session,
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
    db: Db_Session,
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
    db: Db_Session,
) -> None:

    command = DeleteTagCommand(
        SqlAlchemyUnitOfWork(db)
    )
    command.execute(tag_id)