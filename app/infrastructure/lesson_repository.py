from uuid import UUID

from sqlalchemy import func, select, asc, desc
from sqlalchemy.orm import Session

from app.application.lessons.repository import LessonRepository
from app.application.lessons.views import AllLessonsView

from app.models.lesson import Lesson
from app.models.enums import SortBy, SortOrder



class SqlAlchemyLessonRepository(LessonRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_all(
        self,
        page: int,
        page_size: int,
        sort_by: SortBy,
        sort_order: SortOrder
    ) -> AllLessonsView:

        offset = (page - 1) * page_size

        sort_columns = {
            SortBy.CREATED_AT: Lesson.created_at,
            SortBy.UPDATED_AT: Lesson.updated_at,
        }
        sort_column = sort_columns[sort_by]

        order_column = (
            asc(sort_column)
            if sort_order == SortOrder.ASC
            else desc(sort_column)
        )

        total = self.db.scalar(
            select(func.count())
            .select_from(Lesson)
        ) or 0

        statement = (
            select(Lesson)
            .order_by(order_column, Lesson.id)
            .offset(offset)
            .limit(page_size)
        )

        items = list(self.db.scalars(statement).all())

        return AllLessonsView(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=(total + page_size - 1) // page_size,
        )
        

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