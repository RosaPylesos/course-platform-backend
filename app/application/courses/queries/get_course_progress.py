from uuid import UUID

from app.application.exceptions import (
    AccessDeniedError,
    ResourceNotFoundError,
)
from app.application.unit_of_work import UnitOfWork

from app.models.enums import EnrollmentStatus
from app.models.user import User

from app.schemas.lesson_progress import (
    CourseProgressResponse,
    LessonProgressItem,
)



class GetCourseProgressQuery:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def execute(
        self,
        course_id: UUID,
        current_user: User,
    ) -> CourseProgressResponse:
        
        course = self.uow.courses.get_by_id(course_id)

        if course is None:
            raise ResourceNotFoundError("Course not found")

        enrollment = self.uow.enrollments.get_by_user_and_course(
            current_user.id,
            course_id,
        )

        if (
            enrollment is None
            or enrollment.status
            not in (
                EnrollmentStatus.ACTIVE,
                EnrollmentStatus.COMPLETED,
            )
        ):
            raise AccessDeniedError(
                "You must be actively enrolled on this course"
            )

        lessons = self.uow.lessons.list_by_course(course_id)

        progress_records = self.uow.lesson_progress.list_by_enrollment(
            enrollment.id
        )

        progress_by_lesson_id = {
            progress.lesson_id: progress
            for progress in progress_records
        }

        lesson_items = [
            LessonProgressItem(
                lesson_id=lesson.id,
                lesson_name=lesson.name,
                position=lesson.position,
                is_started=lesson.id in progress_by_lesson_id,
                is_completed=(
                    progress_by_lesson_id[lesson.id].is_completed
                    if lesson.id in progress_by_lesson_id
                    else False
                ),
            )
            for lesson in lessons
        ]

        lessons_started = len(progress_records)
        lessons_completed = sum(
            progress.is_completed for progress in progress_records
        )

        return CourseProgressResponse(
            course_id=course.id,
            course_name=course.name,
            course_status=course.status,
            course_difficulty=course.difficulty,
            thumbnail_path=course.thumbnail_path,
            lessons_total=len(lessons),
            lessons_started=lessons_started,
            lessons_completed=lessons_completed,
            lessons=lesson_items,
        )