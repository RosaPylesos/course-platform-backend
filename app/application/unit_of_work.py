from typing import Protocol

from app.application.courses.repository import CourseRepository
from app.application.enrollments.repository import EnrollmentRepository



class UnitOfWork(Protocol):
    courses: CourseRepository
    enrollments: EnrollmentRepository

    def commit(self) -> None:
        ...



    def rollback(self) -> None:
        ...