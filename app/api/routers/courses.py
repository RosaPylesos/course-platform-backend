from uuid import UUID

from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_db, 
    require_roles, 
    get_current_user
)

from app.models.course import Course
from app.models.user import User

from app.models.enums import UserRole

from app.application.courses.queries import (
    GetCoursesQuery,
    GetCourseQuery,
    GetCourseProgressQuery,
    GetMyCoursesQuery,
    GetAllCoursesQuery,
    GetMyCourseQuery,
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
    CourseUpdate
)
from app.schemas.lesson_progress import CourseProgressResponse

router = APIRouter(
    prefix="/courses", 
    tags=["Courses"]
)

@router.get(
    "/", 
    response_model=list[CourseResponse],
    status_code=status.HTTP_200_OK,
)
def get_courses(
    db: Annotated[Session, Depends(get_db)],
) -> list[Course]:
    
    query = GetCoursesQuery(
        SqlAlchemyCourseRepository(db)
    )
    return query.execute()

@router.get(
    "/my",
    response_model=list[CourseResponse],
    status_code=status.HTTP_200_OK,
)
def get_my_courses(
    current_user: Annotated[
        User,
        Depends(
            require_roles(
                UserRole.AUTHOR,
                UserRole.ADMIN,
            )
        ),
    ],
    db: Annotated[Session, Depends(get_db)],
) -> list[Course]:

    query = GetMyCoursesQuery(
        SqlAlchemyCourseRepository(db)
    )
    return query.execute(
        author_id=current_user.id,
    )

@router.get(
    "/my/{course_id}",
    response_model=CourseResponse,
    status_code=status.HTTP_200_OK,
)
def get_my_course(
    course_id: UUID,
    current_user: Annotated[
        User,
        Depends(
            require_roles(
                UserRole.AUTHOR,
                UserRole.ADMIN,
            )
        )
    ],
    db: Annotated[Session, Depends(get_db)],
) -> Course:

    query = GetMyCourseQuery(
        SqlAlchemyCourseRepository(db)
    )
    return query.execute(
        course_id=course_id,
        author_id=current_user.id,
    )

@router.get(
    "/manage",
    response_model=list[CourseResponse],
    status_code=status.HTTP_200_OK,
)
def get_all_courses(
    current_user: Annotated[
        User,
        Depends(require_roles(UserRole.ADMIN)),
    ],
    db: Annotated[Session, Depends(get_db)],
) -> list[Course]:

    query = GetAllCoursesQuery(
        SqlAlchemyCourseRepository(db)
    )
    return query.execute()

@router.get(
    "/{course_id}", 
    response_model=CourseResponse,
    status_code=status.HTTP_200_OK,
)
def get_course(
    course_id: UUID,
    db: Annotated[Session, Depends(get_db)],
) -> Course:
    
    query = GetCourseQuery(
        SqlAlchemyCourseRepository(db)
    )
    return query.execute(course_id=course_id)

@router.get(
    "/{course_id}/progress",
    response_model=CourseProgressResponse,
    status_code=status.HTTP_200_OK,
)
def get_course_progress(
    course_id: UUID,
    current_user: Annotated[
        User, 
        Depends(get_current_user)
    ],
    db: Annotated[Session, Depends(get_db)],
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
    current_user: Annotated[
        User,
        Depends(require_roles(
            UserRole.AUTHOR, 
            UserRole.ADMIN
        )),
    ],
    db: Annotated[Session, Depends(get_db)],

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
    current_user: Annotated[
        User,
        Depends(
            require_roles(
                UserRole.AUTHOR,
                UserRole.ADMIN,
            )
        )
    ],
    db: Annotated[Session, Depends(get_db)],
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
    current_user: Annotated[
        User,
        Depends(
            require_roles(
                UserRole.AUTHOR,
                UserRole.ADMIN,
            )
        )
    ],
    db: Annotated[Session, Depends(get_db)],
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
    current_user: Annotated[
        User,
        Depends(
            require_roles(
                UserRole.AUTHOR,
                UserRole.ADMIN,
            )
        ),
    ],
    db: Annotated[Session, Depends(get_db)],
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
    current_user: Annotated[
        User,
        Depends(
            require_roles(
                UserRole.AUTHOR,
                UserRole.ADMIN,
        )),
    ],
    db: Annotated[Session, Depends(get_db)],
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
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[
        User,
        Depends(
            require_roles(
                UserRole.AUTHOR,
                UserRole.ADMIN,
        )),
    ],
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
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[
        User,
        Depends(
            require_roles(
                UserRole.AUTHOR,
                UserRole.ADMIN,
        )),
    ],
) -> None:

    command = UnassignTagFromCourseCommand(
        SqlAlchemyUnitOfWork(db)
    )
    command.execute(
        course_id=course_id,
        tag_id=tag_id,
        current_user=current_user,
    )