from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

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