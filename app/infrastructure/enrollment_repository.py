from uuid import UUID

from sqlalchemy import select, func, case
from sqlalchemy.orm import Session

from app.application.enrollments.repository import EnrollmentRepository
from app.application.enrollments.views import (
    MyEnrollmentItem,
    EnrollmentProgressSummary,
    MyEnrollmentStatusView,
)
from app.models.enrollment import Enrollment
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.lesson_progress import LessonProgress



class SqlAlchemyEnrollmentRepository(EnrollmentRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_by_user_with_progress(
        self,
        user_id: UUID,
    ) -> list[MyEnrollmentItem]:

        statement = (
            select(
                Enrollment,
                Course,
                func.count(Lesson.id).label("lessons_total"),
                func.count(LessonProgress.id).label("lessons_started"),
                func.coalesce(
                    func.sum(
                        case(
                            (LessonProgress.is_completed.is_(True), 1),
                            else_=0,
                        )
                    ),
                    0,
                ).label("lessons_completed"),
            )
            .join(Course, Enrollment.course_id == Course.id)
            .outerjoin(Lesson, Lesson.course_id == Course.id)
            .outerjoin(
                LessonProgress,
                (LessonProgress.enrollment_id == Enrollment.id)
                & (LessonProgress.lesson_id == Lesson.id),
            )
            .where(Enrollment.user_id == user_id)
            .group_by(Enrollment.id, Course.id)
            .order_by(Enrollment.created_at.desc())
        )

        rows = self.db.execute(statement).all()

        return [
            MyEnrollmentItem(
                id=enrollment.id,
                created_at=enrollment.created_at,
                status=enrollment.status,
                course=course,
                progress=EnrollmentProgressSummary(
                    lessons_total=lessons_total,
                    lessons_started=lessons_started,
                    lessons_completed=lessons_completed,
                ),
            )
            for (
                enrollment, 
                course, 
                lessons_total, 
                lessons_started, 
                lessons_completed
            ) in rows
        ]

    def list_by_course(
        self,
        course_id: UUID,
    ) -> list[Enrollment]:

        statement = select(Enrollment).where(
            Enrollment.course_id == course_id
        )
        return list(self.db.scalars(statement).all())

    def get_by_id_for_user(
        self,
        enrollment_id: UUID,
        user_id: UUID,
    ) -> Enrollment | None:
        
        statement = select(Enrollment).where(
            Enrollment.id == enrollment_id,
            Enrollment.user_id == user_id,
        )

        return self.db.scalar(statement)

    def get_by_user_and_course(
        self,
        user_id: UUID,
        course_id: UUID,
    ) -> Enrollment | None:

        statement = select(Enrollment).where(
            Enrollment.user_id == user_id,
            Enrollment.course_id == course_id,
        )

        return self.db.scalar(statement)

    def add(self, enrollment: Enrollment) -> None:
        self.db.add(enrollment)