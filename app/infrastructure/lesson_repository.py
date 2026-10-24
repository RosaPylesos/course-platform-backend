from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.application.lessons.repository import LessonRepository
from app.models.lesson import Lesson



class SqlAlchemyLessonRepository(LessonRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_by_course(
        self, 
        course_id: UUID
    ) -> list[Lesson]:

        statement = (
            select(Lesson)
            .where(Lesson.course_id == course_id)
            .order_by(Lesson.position)
        )
        return list(self.db.scalars(statement).all())

    def get_by_id_for_course(
        self, 
        lesson_id: UUID, 
        course_id: UUID,
    ) -> Lesson | None:

        statement = select(Lesson).where(
            Lesson.id == lesson_id,
            Lesson.course_id == course_id,
        )
        return self.db.scalar(statement)

    def count_by_course(
        self, 
        course_id: UUID
    ) -> int:

        statement = (
            select(func.count())
            .select_from(Lesson)
            .where(Lesson.course_id == course_id)
        )        
        return self.db.scalar(statement) or 0

    def get_max_position_by_course(
        self, 
        course_id: UUID
    ) -> int | None:

        statement = select(
            func.max(Lesson.position)
        ).where(
            Lesson.course_id == course_id
        )
        return self.db.scalar(statement)

    def add(self, lesson: Lesson) -> None:
        self.db.add(lesson)

    def delete(self, lesson: Lesson) -> None:
        self.db.delete(lesson)