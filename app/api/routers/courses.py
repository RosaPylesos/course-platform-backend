from uuid import UUID

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, require_roles

from app.models.course import Course
from app.models.user import User
from app.models.enums import UserRole, CourseStatus

from app.schemas.course import CourseResponse, CourseCreate, CourseUpdate

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
    
    courses = db.scalars(
        select(Course).where(
            Course.status == CourseStatus.PUBLISHED
        )
    ).all()

    return courses



@router.get(
    "/{course_id}", 
    response_model=CourseResponse,
    status_code=status.HTTP_200_OK,
)
def get_course(
    course_id: UUID,
    db: Annotated[Session, Depends(get_db)],
) -> Course:
    
    statement = select(Course).where(
        Course.id == course_id
    )
    course = db.scalar(statement)

    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )

    if course.status != CourseStatus.PUBLISHED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This course is not published yet"
        )

    return course



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
    
    course = Course(
        **course_data.model_dump(),
        author_id = current_user.id
    )

    db.add(course)
    db.commit()
    db.refresh(course)

    return course



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
    
    course = db.get(Course, course_id)

    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    if (
        current_user.role != UserRole.ADMIN
        and course.author_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only edit your own courses",
        )

    update_data = course_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(course, field, value)

    db.commit()
    db.refresh(course)

    return course



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
    
    course = db.get(Course, course_id)

    if course is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )

    if (
        current_user.role != UserRole.ADMIN
        and course.author_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own courses"
        )

    db.delete(course)
    db.commit()

    return None