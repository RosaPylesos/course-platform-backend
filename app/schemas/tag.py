from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

class TagCreate(BaseModel):
    tag_category_id: UUID
    name: str = Field(
        min_length=1,
        max_length=64,
    )

class TagUpdate(BaseModel):
    tag_category_id: UUID | None = None
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=64,
    )

class TagResponse(BaseModel):
    id: UUID
    tag_category_id: UUID
    name: str
    slug: str

    model_config = ConfigDict(from_attributes=True)

class TagListResponse(BaseModel):
    items: list[TagResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

class PublicTagResponse(BaseModel):
    id: UUID
    name: str
    slug: str

    model_config = ConfigDict(from_attributes=True)