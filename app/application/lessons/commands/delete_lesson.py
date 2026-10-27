from uuid import UUID

from app.application.exceptions import(
    AccessDeniedError,
    ResourceNotFoundError,
)
from app.application.unit_of_work import UnitOfWork

from app.models.enums import UserRole, EnrollmentStatus
from app.models.user import User



class DeleteLessonCommand:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def execute(
        self,
        course_id: UUID,
        lesson_id: UUID,
        user: User,
    ) -> None:
        course = self.uow.courses.get_by_id(course_id)

        if course is None:
            raise ResourceNotFoundError("Course not found")

        if (
            user.role != UserRole.ADMIN
            and course.author_id != user.id
        ):
            raise AccessDeniedError(
                "You can only delete lessons from your own courses"
            )

        lesson = self.uow.lessons.get_by_id_for_course(
            lesson_id=lesson_id,
            course_id=course_id,
        )

        if lesson is None:
            raise ResourceNotFoundError("Lesson not found")

        try:
            self.uow.lessons.delete(lesson)
            self.uow.flush()

            remaining_lessons = self.uow.lessons.list_by_course(course_id)

            max_position = max(
                (item.position for item in remaining_lessons),
                default=0,
            )
            offset = max_position + len(remaining_lessons) + 1

            for item in remaining_lessons:
                item.position += offset

            self.uow.flush()

            for position, item in enumerate(
                remaining_lessons,
                start=1,
            ):
                item.position = position

            lesson_total = len(remaining_lessons)

            if lesson_total > 0:
                enrollments = self.uow.enrollments.list_by_course(course_id)

                for enrollment in enrollments:
                    if enrollment.status != EnrollmentStatus.ACTIVE:
                        continue

                    lessons_completed = (
                        self.uow.lesson_progress.count_completed_by_enrollment(
                            enrollment.id
                        )
                    )

                    if lessons_completed == lesson_total:
                        enrollment.status = EnrollmentStatus.COMPLETED

            self.uow.commit()
        except Exception:
            self.uow.rollback()
            raise