from uuid import UUID

from app.application.unit_of_work import UnitOfWork
from app.application.exceptions import (
    BusinessRuleError,
    ConflictError,
    ResourceNotFoundError,
)

from app.models.enrollment import Enrollment
from app.models.enums import CourseStatus, EnrollmentStatus



class CreateEnrollmentCommand:
    def __init__(
        self,
        uow: UnitOfWork
    ) -> None:
        self.uow = uow

    def execute(
        self,
        user_id: UUID,
        course_id: UUID,
    ) -> Enrollment:
        course = self.uow.courses.get_by_id(course_id)

        if course is None:
            raise ResourceNotFoundError("Course not found")

        if course.status != CourseStatus.PUBLISHED:
            raise BusinessRuleError(
                "Enrollment is only available for published courses"
            )

        existing_enrollment = (
            self.uow.enrollments.get_by_user_and_course(
                user_id,
                course_id
            )
        )

        if existing_enrollment is not None:
            raise ConflictError(
                "You are already enrolled in this course"
            )

        enrollment = Enrollment(
            user_id=user_id,
            course_id=course_id,
            status=EnrollmentStatus.ACTIVE,
        )

        try:
            self.uow.enrollments.add(enrollment)
            self.uow.commit()
            self.uow.refresh(enrollment)
        except Exception:
            self.uow.rollback()
            raise

        return enrollment