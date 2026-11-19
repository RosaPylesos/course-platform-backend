from sqlalchemy.orm import Session

from app.application.unit_of_work import UnitOfWork

from app.infrastructure.user_repository import SqlAlchemyUserRepository
from app.infrastructure.topic_repository import SqlAlchemyTopicRepository
from app.infrastructure.course_repository import SqlAlchemyCourseRepository
from app.infrastructure.enrollment_repository import SqlAlchemyEnrollmentRepository
from app.infrastructure.lesson_progress_repository import SqlAlchemyLessonProgressRepository
from app.infrastructure.lesson_repository import SqlAlchemyLessonRepository
from app.infrastructure.tag_category_repository import SqlAlchemyTagCategoryRepository
from app.infrastructure.tag_repository import SqlAlchemyTagRepository
from app.infrastructure.course_tag_repository import SqlAlchemyCourseTagRepository
from app.infrastructure.user_topic_repository import SqlAlchemyUserTopicRepository



class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, db: Session) -> None:
        self.courses = SqlAlchemyCourseRepository(db)
        self.enrollments = SqlAlchemyEnrollmentRepository(db)
        self.lessons = SqlAlchemyLessonRepository(db)
        self.lesson_progress = SqlAlchemyLessonProgressRepository(db)
        self.topics = SqlAlchemyTopicRepository(db)
        self.users = SqlAlchemyUserRepository(db)
        self.tag_categories = SqlAlchemyTagCategoryRepository(db)
        self.tags = SqlAlchemyTagRepository(db)
        self.course_tags = SqlAlchemyCourseTagRepository(db)
        self.user_topics = SqlAlchemyUserTopicRepository(db)
        self.db = db

    def commit(self) -> None:
        self.db.commit()

    def rollback(self) -> None:
        self.db.rollback()

    def flush(self) -> None:
        self.db.flush()

    def refresh(self, entity: object) -> None:
        self.db.refresh(entity)