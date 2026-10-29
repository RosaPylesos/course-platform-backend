from uuid import UUID
from dataclasses import dataclass

from app.application.courses.repository import CourseRepository
from app.application.courses.views.course_list_item import CourseListItem
from app.application.courses.resolve_catalog_filters import ResolveCatalogFilters

from app.models.enums import CourseDifficulty

@dataclass(frozen=True)
class GetCoursesInput:
    page: int = 1
    page_size: int = 16
    search: str | None = None
    author_id: UUID | None = None
    topics: str | None = None
    tags: str | None = None
    include_descendants: bool = False
    difficulty: CourseDifficulty | None = None



class GetCoursesQuery:
    def __init__(
        self, 
        repository: CourseRepository,
        filter_resolver: ResolveCatalogFilters,
    ) -> None:
        self.repository = repository
        self.filter_resolver = filter_resolver

    def execute(
        self,
        input: GetCoursesInput,
    ) -> tuple[list[CourseListItem], int]:

        topic_ids = (
            self.filter_resolver.resolve_topics(input.topics)
        )
        tags_ids_by_category = (
            self.filter_resolver.resolve_tags(input.tags)
        )
        
        return self.repository.list_published_for_catalog(
            page=input.page,
            page_size=input.page_size,
            search=input.search,
            author_id=input.author_id,
            topic_ids=topic_ids,
            include_descendants=input.include_descendants,
            difficulty=input.difficulty,
            tags_ids_by_category=tags_ids_by_category,
        )