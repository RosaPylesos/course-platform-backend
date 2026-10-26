from uuid import UUID

from app.application.enrollments.repository import EnrollmentRepository
from app.models.enrollment import Enrollment



class GetMyEnrollmentsQuery:
    def __init__(
        self,
        enrollment_repository: EnrollmentRepository,
    ) -> None:
        self.enrollment_repository = enrollment_repository

    def execute(self, user_id: UUID) -> list[Enrollment]:
        return self.enrollment_repository.list_by_user(user_id)