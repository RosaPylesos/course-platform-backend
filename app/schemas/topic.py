from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

class TopicCreate(BaseModel):
    parent_id: UUID | None = None
    name: str = Field(min_length=1, max_length=64)

class TopicUpdate(BaseModel):
    parent_id: UUID | None = None
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=64,
    )

class TopicResponse(BaseModel):
    id: UUID
    parent_id: UUID | None
    name: str
    slug: str

    model_config = ConfigDict(from_attributes=True)

class TopicListResponse(BaseModel):
    items: list[TopicResponse]
    total: int
    page: int
    page_size: int
    total_pages: int