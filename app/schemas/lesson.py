from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.lesson_content import LessonContent

class LessonCreate(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    description: str | None = None
    content: LessonContent = Field(
        default_factory=LessonContent
    )

class LessonUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=64,
    )
    description: str | None = None
    content: LessonContent | None = None

class LessonReorder(BaseModel):
    lesson_ids: list[UUID] = Field(min_length=1)

class LessonResponse(BaseModel):
    id: UUID
    course_id: UUID
    name: str
    description: str | None
    content: LessonContent
    position: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)