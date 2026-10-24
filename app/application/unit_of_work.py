from typing import Protocol

from app.application.courses.repository import CourseRepository
from app.application.enrollments.repository import EnrollmentRepository
from app.application.lessons.repository import LessonRepository
from app.application.lesson_progress.repository import LessonProgressRepository



class UnitOfWork(Protocol):
    courses: CourseRepository
    enrollments: EnrollmentRepository
    lessons: LessonRepository
    lesson_progress: LessonProgressRepository

    def commit(self) -> None:
        ...

    def rollback(self) -> None:
        ...

    def flush(self) -> None:
        ...