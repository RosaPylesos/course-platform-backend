from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import CourseDifficulty, CourseStatus

from app.schemas.tag import TagResponse
from app.schemas.topic import TopicResponse
from app.schemas.author import CourseAuthorResponse

class CourseCreate(BaseModel):
    topic_id: UUID
    name: str = Field(min_length=1, max_length=64)
    description: str | None = None
    difficulty: CourseDifficulty
    thumbnail_path: str | None = None

class CourseUpdate(BaseModel):
    topic_id: UUID | None = None
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=64,
    )
    description: str | None = None
    difficulty: CourseDifficulty | None = None
    thumbnail_path: str | None = None

class CourseResponse(BaseModel):
    id: UUID
    author_id: UUID
    topic_id: UUID
    name: str
    description: str | None
    difficulty: CourseDifficulty
    status: CourseStatus
    thumbnail_path: str | None
    created_at: datetime
    updated_at: datetime
    tags: list[TagResponse] = Field(
        default_factory=list
    )
    
    model_config = ConfigDict(from_attributes=True)

class CourseListItemResponse(BaseModel):
    id: UUID
    name: str
    description: str | None
    difficulty: CourseDifficulty
    thumbnail_path: str | None
    author: CourseAuthorResponse
    topic: TopicResponse
    tags: list[TagResponse] = Field(
        default_factory=list
    )
    lesson_count: int

    model_config = ConfigDict(from_attributes=True)

class CourseListResponse(BaseModel):
    items: list[CourseListItemResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

class CatalogFilterAuthorResponse(BaseModel):
    id: UUID
    name: str
    surname: str | None

class CatalogFilterTopicResponse(BaseModel):
    id: UUID
    name: str
    parent_id: UUID | None
    slug: str

class CatalogFilterTagResponse(BaseModel):
    id: UUID
    name: str
    slug: str

class CatalogFilterTagCategoryResponse(BaseModel):
    id: UUID
    name: str
    tags: list[CatalogFilterTagResponse]

class CourseCatalogFiltersResponse(BaseModel):
    authors: list[CatalogFilterAuthorResponse]
    topics: list[CatalogFilterTopicResponse]
    tag_categories: list[CatalogFilterTagCategoryResponse]
    difficulties: list[CourseDifficulty]