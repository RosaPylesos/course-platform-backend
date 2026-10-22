from uuid import UUID

from sqlalchemy.orm import Session

from app.application.courses.repository import CourseRepository
from app.models.course import Course



class SqlAlchemyCourseRepository(CourseRepository):
    def __init__(self, db: Session) -> None:
        self.db = db



    def get_by_id(self, course_id: UUID) -> Course | None:
        return self.db.get(Course, course_id)