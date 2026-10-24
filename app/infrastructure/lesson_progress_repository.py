from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.application.lesson_progress.repository import(
    LessonProgressRepository,
)
from app.models.lesson_progress import LessonProgress



class SqlAlchemyLessonProgressRepository(
    LessonProgressRepository
):
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_by_enrollment(
        self, 
        enrollment_id: UUID,
    ) -> list[LessonProgress]:

        statement = select(LessonProgress).where(
            LessonProgress.enrollment_id == enrollment_id
        )
        return list(self.db.scalars(statement).all())

    def get_by_enrollment_and_lesson(
        self, 
        enrollment_id: UUID, 
        lesson_id: UUID,
    ) -> LessonProgress | None:
        
        statement = select(LessonProgress).where(
            LessonProgress.enrollment_id == enrollment_id,
            LessonProgress.lesson_id == lesson_id,
        )
        return self.db.scalar(statement)

    def count_completed_by_enrollment(
        self, 
        enrollment_id: UUID,
    ) -> int:

        statement = (
            select(func.count())
            .select_from(LessonProgress)
            .where(
                LessonProgress.enrollment_id == enrollment_id,
                LessonProgress.is_completed.is_(True),
            )
        )
        return self.db.scalar(statement) or 0

    def add(self, progress: LessonProgress) -> None:
        self.db.add(progress)