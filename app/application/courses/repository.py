from typing import Protocol
from uuid import UUID

from app.application.courses.views import (
    CourseCatalogFilters,
    CourseListItem,
) 

from app.models.course import Course
from app.models.enums import CourseDifficulty



class CourseRepository(Protocol):

    def list_all(self) -> list[Course]:
        ...

    def list_published(self) -> list[Course]:
        ...

    def list_published_for_catalog(
        self,
        page: int,
        page_size: int,
        search: str | None = None,
        author_id: UUID | None = None,
        topic_ids:list[UUID] | None = None,
        include_descendants: bool = False,
        difficulty: CourseDifficulty | None = None,
        tags_ids_by_category: dict[UUID, list[UUID]] | None = None,
    ) -> tuple[list[CourseListItem], int]:
        ...

    def get_catalog_filters(self) -> CourseCatalogFilters:
        ...

    def list_by_author(
        self,
        author_id: UUID
    ) -> list[Course]:
        ...

    def get_by_id(self, course_id: UUID) -> Course | None:
        ...

    def add(self, course: Course) -> None:
        ...

    def delete(self, course: Course) -> None:
        ...