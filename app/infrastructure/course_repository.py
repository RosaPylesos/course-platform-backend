from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.application.courses.repository import CourseRepository

from app.models.enums import CourseStatus
from app.models.course import Course



class SqlAlchemyCourseRepository(CourseRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_published(self) -> list[Course]:

        statement = select(Course).where(
            Course.status == CourseStatus.PUBLISHED
        )
        return list(self.db.scalars(statement).all())

    def get_by_id(self, course_id: UUID) -> Course | None:
        return self.db.get(Course, course_id)

    def add(self, course: Course) -> None:
        self.db.add(course)

    def delete(self, course: Course) -> None:
        self.db.delete(course)