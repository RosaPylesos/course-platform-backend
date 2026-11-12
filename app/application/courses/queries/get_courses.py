from uuid import UUID
from dataclasses import dataclass

from app.application.courses.repository import CourseRepository
from app.application.courses.views.course_list import CourseListView
from app.application.courses.resolve_catalog_filters import ResolveCatalogFilters

from app.models.enums import CourseDifficulty

@dataclass(frozen=True)
class GetCoursesInput:
    page: int = 1
    page_size: int = 16
    search: str | None = None
    author_ids: list[UUID] | None = None
    topics: str | None = None
    topic_id: UUID | None = None
    tags: str | None = None
    include_descendants: bool = False
    difficulties: list[CourseDifficulty] | None = None



class GetCoursesQuery:
    def __init__(
        self, 
        course_repository: CourseRepository,
        filter_resolver: ResolveCatalogFilters,
    ) -> None:
        self.course_repository = course_repository
        self.filter_resolver = filter_resolver

    def execute(
        self,
        input: GetCoursesInput,
    ) -> CourseListView:

        topic_ids = (
            self.filter_resolver.resolve_topics(input.topics)
        )
        tags_ids_by_category = (
            self.filter_resolver.resolve_tags(input.tags)
        )
        
        return self.course_repository.list_published_for_catalog(
            page=input.page,
            page_size=input.page_size,
            search=input.search,
            author_ids=input.author_ids,
            topic_ids=topic_ids,
            topic_id=input.topic_id,
            include_descendants=input.include_descendants,
            difficulties=input.difficulties,
            tags_ids_by_category=tags_ids_by_category,
        )