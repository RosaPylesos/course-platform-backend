from sqlalchemy.orm import Session

from app.application.unit_of_work import UnitOfWork

from app.infrastructure.course_repository import SqlAlchemyCourseRepository
from app.infrastructure.enrollment_repository import (
    SqlAlchemyEnrollmentRepository,
)



class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, db: Session) -> None:
        self.courses = SqlAlchemyCourseRepository(db)
        self.enrollments = SqlAlchemyEnrollmentRepository(db)
        self.db = db



    def commit(self) -> None:
        self.db.commit()



    def rollback(self) -> None:
        self.db.rollback()