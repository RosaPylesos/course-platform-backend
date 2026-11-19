from typing import Protocol
from uuid import UUID

from app.application.courses.views import (
    CourseCatalogFiltersView,
    CourseListView,
    HomePageSectionView,
    MyCoursesView,
    AllCoursesView,
)

from app.models.course import Course
from app.models.enums import (
    CourseDifficulty, 
    CourseStatus,
    SortBy,
    SortOrder,
)



class CourseRepository(Protocol):

    def list_all(
        self,
        page: int,
        page_size: int,
        sort_by: SortBy,
        sort_order: SortOrder
    ) -> AllCoursesView:
        ...

    def get_home_page_sections(
        self,
        preferred_topic_ids: list[UUID] | None = None,
        limit_topics: int = 5,
        courses_per_topic: int = 5,
    ) -> list[HomePageSectionView]:
        ...

    def list_published_for_catalog(
        self,
        page: int,
        page_size: int,
        search: str | None = None,
        author_id: UUID | None = None,
        topic_ids:list[UUID] | None = None,
        topic_id: UUID | None = None,
        include_descendants: bool = False,
        difficulty: CourseDifficulty | None = None,
        tags_ids_by_category: dict[UUID, list[UUID]] | None = None,
    ) -> CourseListView:
        ...

    def get_catalog_filters(
        self,
        topic_id: UUID | None = None,
    ) -> CourseCatalogFiltersView:
        ...

    def list_by_author(
        self,
        author_id: UUID,
        page: int,
        page_size: int,
        status: CourseStatus | None = None,
    ) -> MyCoursesView:
        ...

    def get_by_id(self, course_id: UUID) -> Course | None:
        ...

    def get_by_id_with_relations(
        self,
        course_id: UUID
    ) -> Course | None:
        ...

    def get_detail(self, course_id: UUID) -> Course | None:
        ...

    def add(self, course: Course) -> None:
        ...

    def delete(self, course: Course) -> None:
        ...