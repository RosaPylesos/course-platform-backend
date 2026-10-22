from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

class LessonProgressItem(BaseModel):
    lesson_id: UUID
    lesson_name: str
    is_started: bool
    is_completed: bool

class CourseProgressResponse(BaseModel):
    course_id: UUID
    lessons_total: int
    lessons_started: int
    lessons_completed: int
    lessons: list[LessonProgressItem]

class LessonProgressResponse(BaseModel):
    id: UUID
    enrollment_id: UUID
    lesson_id: UUID
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)