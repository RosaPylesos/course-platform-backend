from typing import Protocol
from uuid import UUID

from app.models.enrollment import Enrollment



class EnrollmentRepository(Protocol):

    def list_by_user(
        self, 
        user_id: UUID
    ) -> list[Enrollment]:
        ...

    def list_by_course(
        self, 
        course_id: UUID
    ) -> list[Enrollment]:
        ...

    def get_by_id_for_user(
        self,
        enrollment_id: UUID,
        user_id: UUID
    ) -> Enrollment | None:
        ...

    def get_by_user_and_course(
        self,
        user_id: UUID,
        course_id: UUID
    ) -> Enrollment | None:
        ...

    def add(self, enrollment: Enrollment) -> None:
        ...