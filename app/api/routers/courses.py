from uuid import UUID

from typing import Annotated

from fastapi import (
    APIRouter, 
    Depends, 
    status, 
    Query,
)

from app.api.schemas.course_catalog import CourseCatalogParams
from app.api.schemas.my_course import MyCoursesParams

from app.api.deps.courses import (
    get_my_courses_query,
    get_my_course_query,
    get_course_catalog_query,
)

from app.api.dependencies import (
    Db_Session,
    Author_Or_Admin_User, 
    Current_User,
)
from app.api.mappers.course_mapper import (
    to_course_list_response,
    to_course_list_item_response,
    to_course_catalog_filters_response,
    to_my_courses_response,
    to_my_course_detail_response,
)

from app.models.course import Course

from app.application.courses.queries import (
    GetCoursesQuery,
    GetCourseQuery,
    GetCourseProgressQuery,
    GetMyCoursesQuery,
    GetMyCourseQuery,
    GetCourseCatalogFiltersQuery,
    GetCoursesInput,
    GetMyCoursesInput,
)
from app.application.courses.commands import (
    CreateCourseCommand,
    UpdateCourseCommand,
    DeleteCourseCommand,
    PublishCourseCommand,
    ArchiveCourseCommand,
)
from app.application.course_tags.commands import(
    AssignTagToCourseCommand,
    UnassignTagFromCourseCommand,
)

from app.infrastructure.course_repository import (
    SqlAlchemyCourseRepository,
)
from app.infrastructure.unit_of_work import (
    SqlAlchemyUnitOfWork,
)

from app.schemas.course import (
    CourseResponse, 
    CourseCreate, 
    CourseUpdate,
    CourseListResponse,
    CourseListItemResponse,
    CourseCatalogFiltersResponse,
    MyCourseListResponse,
    MyCourseDetailResponse,
)
from app.schemas.lesson_progress import CourseProgressResponse

router = APIRouter(
    prefix="/courses", 
    tags=["Courses"]
)

@router.get(
    "/", 
    response_model=CourseListResponse,
    status_code=status.HTTP_200_OK,
)
def get_courses(
    query: Annotated[
        GetCoursesQuery,
        Depends(get_course_catalog_query)
    ],
    params: Annotated[
        CourseCatalogParams, Query()
    ],
) -> CourseListResponse:

    input = GetCoursesInput(**params.model_dump())
    result = query.execute(input)
    
    return to_course_list_response(result)

@router.get(
    "/filters",
    response_model=CourseCatalogFiltersResponse,
    status_code=status.HTTP_200_OK,
)
def get_course_catalog_filters(
    db: Db_Session,
) -> CourseCatalogFiltersResponse:

    query = GetCourseCatalogFiltersQuery(
        SqlAlchemyCourseRepository(db),
    )

    result = query.execute()
    return to_course_catalog_filters_response(result)

@router.get(
    "/my",
    response_model=MyCourseListResponse,
    status_code=status.HTTP_200_OK,
)
def get_my_courses(
    current_user: Author_Or_Admin_User,
    query: Annotated[
        GetMyCoursesQuery,
        Depends(get_my_courses_query),
    ],
    params: Annotated[
        MyCoursesParams, 
        Depends(),
    ],
) -> MyCourseListResponse:

    input = GetMyCoursesInput(**params.model_dump())

    result = query.execute(
        author_id=current_user.id,
        input=input,
    )
    return to_my_courses_response(result)

@router.get(
    "/my/{course_id}",
    response_model=MyCourseDetailResponse,
    status_code=status.HTTP_200_OK,
)
def get_my_course(
    course_id: UUID,
    current_user: Author_Or_Admin_User,
    query: Annotated[
        GetMyCourseQuery,
        Depends(get_my_course_query),
    ],
) -> MyCourseDetailResponse:

    course = query.execute(
        course_id=course_id,
        author_id=current_user.id,
    )
    return to_my_course_detail_response(course)

@router.get(
    "/{course_id}", 
    response_model=CourseListItemResponse,
    status_code=status.HTTP_200_OK,
)
def get_course(
    course_id: UUID,
    db: Db_Session,
) -> CourseListItemResponse:
    
    query = GetCourseQuery(
        SqlAlchemyCourseRepository(db)
    )
    item = query.execute(course_id=course_id)
    return to_course_list_item_response(item)

@router.get(
    "/{course_id}/progress",
    response_model=CourseProgressResponse,
    status_code=status.HTTP_200_OK,
)
def get_course_progress(
    course_id: UUID,
    current_user: Current_User,
    db: Db_Session,
) -> CourseProgressResponse:

    query = GetCourseProgressQuery(
        SqlAlchemyUnitOfWork(db)
    )
    return query.execute(
        course_id=course_id,
        current_user=current_user,
    )

@router.post(
    "/", 
    response_model=CourseResponse, 
    status_code=status.HTTP_201_CREATED,
)
def create_course(
    course_data: CourseCreate,
    current_user: Author_Or_Admin_User,
    db: Db_Session,

) -> Course:
    
    command = CreateCourseCommand(
        SqlAlchemyUnitOfWork(db)
    )
    return command.execute(
        course_data=course_data,
        author_id=current_user.id,
    )

@router.patch(
    "/{course_id}", 
    response_model=CourseResponse,
    status_code=status.HTTP_200_OK,
)
def update_course(
    course_id: UUID,
    course_data: CourseUpdate,
    current_user: Author_Or_Admin_User,
    db: Db_Session,
) -> Course:
    
    command = UpdateCourseCommand(
        SqlAlchemyUnitOfWork(db)
    )
    return command.execute(
        course_id=course_id,
        course_data=course_data,
        current_user=current_user
    )

@router.post(
    "/{course_id}/publish",
    response_model=CourseResponse,
    status_code=status.HTTP_200_OK,
)
def publish_course(
    course_id: UUID,
    current_user: Author_Or_Admin_User,
    db: Db_Session,
) -> Course:

    command = PublishCourseCommand(
        SqlAlchemyUnitOfWork(db)
    )
    return command.execute(
        course_id=course_id,
        current_user=current_user,
    )

@router.post(
    "/{course_id}/archive",
    response_model=CourseResponse,
    status_code=status.HTTP_200_OK,
)
def archive_course(
    course_id: UUID,
    current_user: Author_Or_Admin_User,
    db: Db_Session,
) -> Course:

    command = ArchiveCourseCommand(
        SqlAlchemyUnitOfWork(db)
    )
    return command.execute(
        course_id=course_id,
        current_user=current_user,
    )

@router.delete("/{course_id}", status_code=204)
def delete_course(
    course_id: UUID,
    current_user: Author_Or_Admin_User,
    db: Db_Session,
) -> None:
    
    command = DeleteCourseCommand(
        SqlAlchemyUnitOfWork(db)
    )
    command.execute(
        course_id=course_id,
        current_user=current_user,
    )

@router.post(
    "/{course_id}/tags/{tag_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def assign_tag_to_course(
    course_id: UUID,
    tag_id: UUID,
    db: Db_Session,
    current_user: Author_Or_Admin_User,
) -> None:

    command = AssignTagToCourseCommand(
        SqlAlchemyUnitOfWork(db)
    )
    command.execute(
        course_id=course_id,
        tag_id=tag_id,
        current_user=current_user,
    )

@router.delete(
    "/{course_id}/tags/{tag_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def unassign_tag_from_course(
    course_id: UUID,
    tag_id: UUID,
    db: Db_Session,
    current_user: Author_Or_Admin_User,
) -> None:

    command = UnassignTagFromCourseCommand(
        SqlAlchemyUnitOfWork(db)
    )
    command.execute(
        course_id=course_id,
        tag_id=tag_id,
        current_user=current_user,
    )