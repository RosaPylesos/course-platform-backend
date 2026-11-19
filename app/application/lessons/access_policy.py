from uuid import UUID

from app.application.exceptions import (
    AccessDeniedError,
    ResourceNotFoundError,
)
from app.application.unit_of_work import UnitOfWork

from app.models.course import Course
from app.models.enums import (
    CourseStatus, 
    EnrollmentStatus, 
    UserRole
)
from app.models.user import User



class LessonAccessPolicy:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def check_course_access(
        self,
        course_id: UUID,
        user: User,
    ) -> Course:
        course = self.uow.courses.get_by_id(course_id)

        if course is None:
            raise ResourceNotFoundError("Course not found")

        if user.role == UserRole.ADMIN:
            return course

        if (
            user.role == UserRole.AUTHOR
            and course.author_id == user.id
        ):
            return course

        if course.status != CourseStatus.PUBLISHED:
            raise AccessDeniedError("This course is not available")

        enrollment = self.uow.enrollments.get_by_user_and_course(
            user.id,
            course_id,
        )

        if(
            enrollment is None
            or enrollment.status
            not in (
                EnrollmentStatus.ACTIVE,
                EnrollmentStatus.COMPLETED,
            )
        ):
            raise AccessDeniedError(
                "You must be actively enrolled in this course"
            )

        return course