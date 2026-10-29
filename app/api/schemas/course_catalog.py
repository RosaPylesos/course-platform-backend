from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import CourseDifficulty



class CourseCatalogParams(BaseModel):
    model_config = ConfigDict(extra="forbid")

    page: int = Field(default=1, ge=1)
    page_size: int = Field(
        default=16,
        ge=1,
        le=100,
    )
    search: str | None = Field(
        default=None,
        max_length=100,
    )
    author_id: UUID | None = None
    topics: str | None = Field(
        default=None,
        max_length=500,
    )
    tags: str | None = Field(
        default=None,
        max_length=500,
    )
    include_descendants: bool = False
    difficulty: CourseDifficulty | None = None