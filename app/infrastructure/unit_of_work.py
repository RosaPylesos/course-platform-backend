from sqlalchemy.orm import Session

from app.application.unit_of_work import UnitOfWork

from app.infrastructure import (
    SqlAlchemyCourseRepository,
    SqlAlchemyLessonRepository,
    SqlAlchemyEnrollmentRepository,
    SqlAlchemyLessonProgressRepository,
    SqlAlchemyTopicRepository,
    SqlAlchemyUserRepository,
)



class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, db: Session) -> None:
        self.courses = SqlAlchemyCourseRepository(db)
        self.enrollments = SqlAlchemyEnrollmentRepository(db)
        self.lessons = SqlAlchemyLessonRepository(db)
        self.lesson_progress = SqlAlchemyLessonProgressRepository(db)
        self.topics = SqlAlchemyTopicRepository(db)
        self.users = SqlAlchemyUserRepository(db)
        self.db = db

    def commit(self) -> None:
        self.db.commit()

    def rollback(self) -> None:
        self.db.rollback()

    def flush(self) -> None:
        self.db.flush()

    def refresh(self, entity: object) -> None:
        self.db.refresh(entity)