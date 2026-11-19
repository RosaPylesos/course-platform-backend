from uuid import UUID

from fastapi import APIRouter, status

from app.api.dependencies import Current_User, Db_Session
from app.api.mappers.enrollment_mapper import (
    to_my_enrollments_response,
)

from app.models.enrollment import Enrollment

from app.application.enrollments.queries import (
    GetMyEnrollmentsQuery,
    GetMyEnrollmentStatusQuery,
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
    EnrollmentStatusResponse,
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
    db: Db_Session,
    current_user: Current_User,
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
    db: Db_Session,
    current_user: Current_User,
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
    db: Db_Session,
    current_user: Current_User,
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
    db: Db_Session,
    current_user: Current_User,
) -> Enrollment:
    
    command = RestoreEnrollmentCommand(
        SqlAlchemyUnitOfWork(db)
    )

    return command.execute(
        enrollment_id=enrollment_id,
        user_id=current_user.id,
    )

@router.get(
    "/status/{course_id}",
    response_model=EnrollmentStatusResponse,
    status_code=status.HTTP_200_OK,
)
def get_my_enrollment_status(
    course_id: UUID,
    db: Db_Session,
    current_user: Current_User,
) -> EnrollmentStatusResponse:

    query = GetMyEnrollmentStatusQuery(
        SqlAlchemyEnrollmentRepository(db),
    )
    return query.execute(
        course_id=course_id,
        user_id=current_user.id,
    )