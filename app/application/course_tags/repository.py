from typing import Protocol
from uuid import UUID

from app.models.course_tag import CourseTag



class CourseTagRepository(Protocol):

    def get_by_ids(
        self,
        course_id: UUID,
        tag_id: UUID,
    ) -> CourseTag | None:
        ...

    def add(
        self,
        course_tag: CourseTag,
    ) -> None: ...

    def delete(
        self,
        course_tag: CourseTag,
    ) -> None: ...