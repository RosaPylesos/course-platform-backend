from app.application.courses.views import (
    CourseCatalogFilters,
    CourseListItem,
    HomePageSection,
    MyCoursesView,
)

from app.models.course import Course

from app.schemas.course import (
    CourseListItemResponse,
    CourseCatalogFiltersResponse,
    CatalogFilterTagCategoryResponse,
    CatalogFilterTopicResponse,
    CatalogFilterAuthorResponse,
    CatalogFilterTagResponse,
    MyCourseListResponse,
    MyCourseListItemResponse,
    MyCourseDetailResponse,
)
from app.schemas.home_page import (
    HomePageResponse,
    HomePageSectionResponse,
)
from app.schemas.topic import TopicResponse
from app.schemas.tag import TagResponse



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

def to_my_courses_response(
    view: MyCoursesView,
) -> MyCourseListResponse:

    return MyCourseListResponse(
        items=[
            MyCourseListItemResponse(
                id=course.id,
                name=course.name,
                status=course.status,
                thumbnail_path=course.thumbnail_path,
                topic=TopicResponse.model_validate(course.topic),
                tags=[
                    TagResponse.model_validate(course_tag.tag)
                    for course_tag in course.course_tags
                ],
                created_at=course.created_at,
                updated_at=course.updated_at,
            )
            for course in view.items
        ],
        total=view.total,
        page=view.page,
        page_size=view.page_size,
        total_pages=view.total_pages,
        status_counts=view.status_counts,
    )

def to_my_course_detail_response(
    course: Course,
) -> MyCourseDetailResponse:

    return MyCourseDetailResponse(
        id=course.id,
        name=course.name,
        description=course.description,
        difficulty=course.difficulty,
        status=course.status,
        thumbnail_path=course.thumbnail_path,
        topic=TopicResponse.model_validate(course.topic),
        tags=[
            TagResponse.model_validate(course_tag.tag)
            for course_tag in course.course_tags
        ],
        created_at=course.created_at,
        updated_at=course.updated_at,
    )