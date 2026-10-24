from uuid import UUID

from app.application.unit_of_work import UnitOfWork
from app.application.exceptions import (
    ConflictError,
    ResourceNotFoundError,
)

from app.models.enrollment import Enrollment
from app.models.enums import EnrollmentStatus



class CancelEnrollmentCommand:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow



    def execute(
        self,
        enrollment_id: UUID,
        user_id: UUID,
    ) -> Enrollment:
        enrollment = self.uow.enrollments.get_by_id_for_user(
            enrollment_id,
            user_id,
        )

        if enrollment is None:
            raise ResourceNotFoundError("Enrollment not found")

        if enrollment.status != EnrollmentStatus.ACTIVE:
            raise ConflictError(
                "Only active enrollments can be cancelled"
            )

        enrollment.status = EnrollmentStatus.CANCELLED

        try:
            self.uow.commit()
        except Exception:
            self.uow.rollback()
            raise

        return enrollment