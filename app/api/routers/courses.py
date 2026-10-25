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
)
from app.application.courses.commands import (
    CreateCourseCommand,
    UpdateCourseCommand,
    DeleteCourseCommand,
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