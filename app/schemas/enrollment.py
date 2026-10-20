from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.enums import EnrollmentStatus

class EntrollmentCreate(BaseModel):
    course_id: UUID

class EnrollmentResponse(BaseModel):
    id: UUID
    user_id: UUID
    course_id: UUID
    status: EnrollmentStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)