from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.enums import EnrollmentStatus, CourseStatus

class EnrollmentCreate(BaseModel):
    course_id: UUID

class EnrollmentResponse(BaseModel):
    id: UUID
    user_id: UUID
    course_id: UUID
    status: EnrollmentStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class EnrollmentCourseSummaryResponse(BaseModel):
    id: UUID
    name: str
    thumbnail_path: str | None
    status: CourseStatus

    model_config = ConfigDict(from_attributes=True)

class EnrollmentProgressSummaryResponse(BaseModel):
    lessons_total: int
    lessons_started: int
    lessons_completed: int

class MyEnrollmentItemResponse(BaseModel):
    id: UUID
    created_at: datetime
    course: EnrollmentCourseSummaryResponse
    progress: EnrollmentProgressSummaryResponse

    model_config = ConfigDict(from_attributes=True)

class EnrollmentStatusGroupResponse(BaseModel):
    status: EnrollmentStatus
    count: int
    items: list[MyEnrollmentItemResponse]

class MyEnrollmentsResponse(BaseModel):
    status_counts: dict[EnrollmentStatus, int]
    groups: list[EnrollmentStatusGroupResponse]