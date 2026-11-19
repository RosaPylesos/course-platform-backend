from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.application.course_tags.repository import CourseTagRepository

from app.models.course_tag import CourseTag



class SqlAlchemyCourseTagRepository(CourseTagRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_ids(
        self,
        course_id: UUID,
        tag_id: UUID,
    ) -> CourseTag | None:

        statement = select(CourseTag).where(
            CourseTag.course_id == course_id,
            CourseTag.tag_id == tag_id,
        )
        return self.db.scalar(statement)

    def add(
        self,
        course_tag: CourseTag,
    ) -> None:

        self.db.add(course_tag)

    def delete(
        self,
        course_tag: CourseTag,
    ) -> None:

        self.db.delete(course_tag)