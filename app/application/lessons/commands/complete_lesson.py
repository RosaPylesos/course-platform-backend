from uuid import UUID

from app.application.exceptions import(
    AccessDeniedError,
    BusinessRuleError,
    ResourceNotFoundError,
)
from app.application.unit_of_work import UnitOfWork

from app.models.enums import CourseStatus, EnrollmentStatus
from app.models.lesson_progress import LessonProgress
from app.models.user import User



class CompleteLessonCommand:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def execute(
        self,
        course_id: UUID,
        lesson_id: UUID,
        user: User,
    ) -> LessonProgress:
        course = self.uow.courses.get_by_id(course_id)

        if course is None:
            raise ResourceNotFoundError("Course not found")

        lesson = self.uow.lessons.get_by_id_for_course(
            lesson_id=lesson_id,
            course_id=course_id,
        )

        if lesson is None:
            raise ResourceNotFoundError("Lesson not found")

        if course.status != CourseStatus.PUBLISHED:
            raise AccessDeniedError("This course is not available")

        enrollment = self.uow.enrollments.get_by_user_and_course(
            user_id=user.id,
            course_id=course_id,
        )

        if(
            enrollment is None
            or enrollment.status != EnrollmentStatus.ACTIVE
        ):
            raise AccessDeniedError(
                "You must be actively enrolled in this course"
            )

        progress = self.uow.lesson_progress.get_by_enrollment_and_lesson(
            enrollment_id=enrollment.id,
            lesson_id=lesson_id,
        )

        if progress is None:
            raise BusinessRuleError(
                "Lesson must be started before it can be completed"
            )

        try:
            if not progress.is_completed:
                progress.is_completed = True

            self.uow.flush()

            lessons_total = self.uow.lessons.count_by_course(course_id)
            lessons_completed = (
                self.uow.lesson_progress.count_completed_by_enrollment(
                    enrollment.id
                )
            )

            if(
                lessons_total > 0
                and lessons_completed == lessons_total
            ):
                enrollment.status = EnrollmentStatus.COMPLETED

            self.uow.commit()

        except Exception:
            self.uow.rollback()
            raise

        return progress