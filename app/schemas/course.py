from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import CourseDifficulty, CourseStatus

class CourseCreate(BaseModel):
    author_id: UUID
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
        max_length=64
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
    
    model_config = ConfigDict(from_attributes=True)