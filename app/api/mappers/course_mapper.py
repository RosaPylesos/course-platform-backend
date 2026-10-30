from app.application.courses.views import (
    CourseCatalogFilters,
    CourseListItem,
    HomePageSection,
)

from app.schemas.course import (
    CourseListItemResponse,
    CourseCatalogFiltersResponse,
    CatalogFilterTagCategoryResponse,
    CatalogFilterTopicResponse,
    CatalogFilterAuthorResponse,
    CatalogFilterTagResponse
)
from app.schemas.home_page import (
    HomePageResponse,
    HomePageSectionResponse,
)



def to_course_list_item_response(
    item: CourseListItem,
) -> CourseListItemResponse:
    return CourseListItemResponse(
        id=item.course.id,
        name=item.course.name,
        description=item.course.description,
        difficulty=item.course.difficulty,
        thumbnail_path=item.course.thumbnail_path,
        author=item.course.author,
        topic=item.course.topic,
        tags=[
            course_tag.tag for course_tag in item.course.course_tags
        ],
        lesson_count=item.lesson_count
    )

def to_course_catalog_filters_response(
    filters: CourseCatalogFilters
) -> CourseCatalogFiltersResponse:
    return CourseCatalogFiltersResponse(
        authors=[
            CatalogFilterAuthorResponse(
                id=author.id,
                name=author.name,
                surname=author.surname,
            )
            for author in filters.authors
        ],
        topics =[
            CatalogFilterTopicResponse(
                id=topic.id,
                name=topic.name,
                parent_id=topic.parent_id,
                slug=topic.slug,
            )
            for topic in filters.topics
        ],
        tag_categories=[
            CatalogFilterTagCategoryResponse(
                id=category.id,
                name=category.name,
                tags=[
                    CatalogFilterTagResponse(
                        id=tag.id,
                        name=tag.name,
                        slug=tag.slug,
                    )
                    for tag in category.tags
                ],
            )
            for category in filters.tag_categories
        ],
        difficulties=filters.difficulties,
    )

def to_home_page_response(
    sections: list[HomePageSection],
) -> HomePageResponse:
    return HomePageResponse(
        sections=[
            HomePageSectionResponse(
                topic=section.topic,
                courses=[
                    to_course_list_item_response(course)
                    for course in section.courses
                ],
            )
            for section in sections
        ]
    )