from uuid import UUID

from typing import Annotated

from fastapi import APIRouter, Depends, status

from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.api.mappers.enrollment_mapper import (
    to_my_enrollments_response,
)

from app.models.enrollment import Enrollment
from app.models.user import User

from app.application.enrollments.queries import (
    GetMyEnrollmentsQuery,
)
from app.application.enrollments.commands import(
    CreateEnrollmentCommand,
    CancelEnrollmentCommand,
    RestoreEnrollmentCommand,
)

from app.infrastructure.enrollment_repository import(
    SqlAlchemyEnrollmentRepository,
)
from app.infrastructure.unit_of_work import SqlAlchemyUnitOfWork

from app.schemas.enrollment import (
    EnrollmentCreate, 
    EnrollmentResponse,
    MyEnrollmentsResponse,
)

router = APIRouter(
    prefix="/enrollments",
    tags=["Enrollments"],
)

@router.get(
    "/",
    response_model=MyEnrollmentsResponse,
    status_code=status.HTTP_200_OK,
)
def get_my_enrollments(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> MyEnrollmentsResponse:

    view = GetMyEnrollmentsQuery(
        SqlAlchemyEnrollmentRepository(db)
    ).execute(current_user.id)
    return to_my_enrollments_response(view)

@router.post(
    "/",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_enrollment(
    enrollment_data: EnrollmentCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Enrollment:

    command = CreateEnrollmentCommand(
        SqlAlchemyUnitOfWork(db)
    )

    return command.execute(
        user_id=current_user.id,
        course_id=enrollment_data.course_id,
    )

@router.patch(
    "/{enrollment_id}/cancel",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_200_OK,
)
def cancel_enrollment(
    enrollment_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Enrollment:

    command = CancelEnrollmentCommand(
        SqlAlchemyUnitOfWork(db)
    )

    return command.execute(
        enrollment_id=enrollment_id,
        user_id=current_user.id,
    )

@router.patch(
    "/{enrollment_id}/restore",
    response_model=EnrollmentResponse,
    status_code=status.HTTP_200_OK,
)
def restore_enrollment(
    enrollment_id: UUID,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Enrollment:
    
    command = RestoreEnrollmentCommand(
        SqlAlchemyUnitOfWork(db)
    )

    return command.execute(
        enrollment_id=enrollment_id,
        user_id=current_user.id,
    )