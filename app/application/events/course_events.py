from dataclasses import dataclass
from uuid import UUID



@dataclass(frozen=True)
class CourseCompleted:
    enrollment_id: UUID
    user_id: UUID
    course_id: UUID