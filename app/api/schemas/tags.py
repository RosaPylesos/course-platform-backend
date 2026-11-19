from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict



class TagCategoryListParams(BaseModel):
    model_config = ConfigDict(extra="forbid")

    page: int = Field(default=1, ge=1)
    page_size: int = Field(
        default=20,
        ge=1,
        le=100,
    )

class TagListParams(BaseModel):
    model_config = ConfigDict(extra="forbid")

    page: int = Field(default=1, ge=1)
    page_size: int = Field(
        default=20,
        ge=1,
        le=100,
    )
    tag_category_id: UUID | None = None