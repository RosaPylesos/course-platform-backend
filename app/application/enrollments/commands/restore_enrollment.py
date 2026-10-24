from uuid import UUID

from app.application.exceptions import (
    ConflictError,
    ResourceNotFoundError,
)
from app.application.unit_of_work import UnitOfWork

from app.models.enrollment import Enrollment
from app.models.enums import (
    CourseStatus,
    EnrollmentStatus,
)



class RestoreEnrollmentCommand:
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

        if enrollment.status != EnrollmentStatus.CANCELLED:
            raise ConflictError(
                "Only cancelled enrollments can be restored"
            )

        enrollment.status = EnrollmentStatus.ACTIVE

        course = self.uow.courses.get_by_id(enrollment.course_id)

        if course is not None and course.status == CourseStatus.PUBLISHED:
            lessons_total = self.uow.lessons.count_by_course(
                enrollment.course_id,
            )

            lessons_completed = (
                self.uow.lesson_progress.count_completed_by_enrollment(
                    enrollment.id,
                )
            )

            if (
                lessons_total > 0
                and lessons_completed == lessons_total
            ):
                enrollment.status = EnrollmentStatus.COMPLETED

        try:
            self.uow.commit()
        except Exception:
            self.uow.rollback()
            raise

        return enrollment