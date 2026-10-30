from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.models.enums import EnrollmentStatus
from app.models.course import Course



@dataclass(frozen=True)
class EnrollmentProgressSummary:
    lessons_total: int
    lessons_started: int
    lessons_completed: int

@dataclass(frozen=True)
class MyEnrollmentItem:
    id: UUID
    created_at: datetime
    status: EnrollmentStatus
    course: Course
    progress: EnrollmentProgressSummary

@dataclass(frozen=True)
class EnrollmentStatusGroup:
    status: EnrollmentStatus
    count: int
    items: list[MyEnrollmentItem]

@dataclass(frozen=True)
class MyEnrollmentsView:
    status_counts: dict[EnrollmentStatus, int]
    groups: list[EnrollmentStatusGroup]