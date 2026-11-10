from uuid import UUID
from dataclasses import dataclass

from app.models.enums import EnrollmentStatus



@dataclass(frozen=True)
class MyEnrollmentStatusView:
    id: UUID
    course_id: UUID
    status: EnrollmentStatus