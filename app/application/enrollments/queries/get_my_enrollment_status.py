from dataclasses import dataclass
from uuid import UUID

from app.application.exceptions import ResourceNotFoundError
from app.application.enrollments.repository import EnrollmentRepository
from app.application.enrollments.views import MyEnrollmentStatusView



class GetMyEnrollmentStatusQuery:
    def __init__(
        self,
        enrollment_repository: EnrollmentRepository,
    ) -> None:
        self.enrollment_repository = enrollment_repository

    def execute(
        self,
        course_id: UUID,
        user_id: UUID,
    ) -> MyEnrollmentStatusView:

        enrollment = self.enrollment_repository.get_by_user_and_course(
            user_id=user_id,
            course_id=course_id,
        )

        if enrollment is None:
            raise ResourceNotFoundError("Enrollment not found")

        return MyEnrollmentStatusView(
            id=enrollment.id,
            course_id=enrollment.course_id,
            status=enrollment.status,
        )