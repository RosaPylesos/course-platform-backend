from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.tag import PublicTagResponse

class TagCategoryCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=64,
    )

class TagCategoryUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=64,
    )

class TagCategoryResponse(BaseModel):
    id: UUID
    name: str
    slug: str

    model_config = ConfigDict(from_attributes=True)

class TagCategoryListResponse(BaseModel):
    items: list[TagCategoryResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

class PublicTagCategoryResponse(BaseModel):
    id: UUID
    name: str
    tags: list[PublicTagResponse]

    model_config = ConfigDict(from_attributes=True)