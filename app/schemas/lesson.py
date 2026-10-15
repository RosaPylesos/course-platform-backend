from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

class LessonCreate(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    description: str | None = None
    content: dict = Field(default_factory=dict)

class LessonUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=64,
    )
    description: str | None = None
    content: dict | None = None

class LessonResponse(BaseModel):
    id: UUID
    course_id: UUID
    name: str
    description: str | None
    content: dict
    position: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)