from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.application.enrollments.repository import EnrollmentRepository
from app.models.enrollment import Enrollment



class SqlAlchemyEnrollmentRepository(EnrollmentRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_by_user(
        self, 
        user_id: UUID
    ) -> list[Enrollment]:

        statement = select(Enrollment).where(
            Enrollment.user_id == user_id
        )

        return list(
            self.db.scalars(statement).all()
        )

    def list_by_course(
        self,
        course_id: UUID,
    ) -> list[Enrollment]:

        statement = select(Enrollment).where(
            Enrollment.course_id == course_id
        )
        return list(self.db.scalars(statement).all())

    def get_by_id_for_user(
        self,
        enrollment_id: UUID,
        user_id: UUID,
    ) -> Enrollment | None:
        
        statement = select(Enrollment).where(
            Enrollment.id == enrollment_id,
            Enrollment.user_id == user_id,
        )

        return self.db.scalar(statement)

    def get_by_user_and_course(
        self,
        user_id: UUID,
        course_id: UUID,
    ) -> Enrollment | None:

        statement = select(Enrollment).where(
            Enrollment.user_id == user_id,
            Enrollment.course_id == course_id,
        )

        return self.db.scalar(statement)

    def add(self, enrollment: Enrollment) -> None:
        self.db.add(enrollment)