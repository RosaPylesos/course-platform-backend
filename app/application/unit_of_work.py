from typing import Protocol

from app.application.courses.repository import CourseRepository
from app.application.enrollments.repository import EnrollmentRepository
from app.application.lessons.repository import LessonRepository
from app.application.lesson_progress.repository import LessonProgressRepository
from app.application.topics.repository import TopicRepository
from app.application.users.repository import UserRepository
from app.application.tag_categories.repository import TagCategoryRepository
from app.application.tags.repository import TagRepository
from app.application.course_tags.repository import CourseTagRepository



class UnitOfWork(Protocol):
    courses: CourseRepository
    enrollments: EnrollmentRepository
    lessons: LessonRepository
    lesson_progress: LessonProgressRepository
    topics: TopicRepository
    users: UserRepository
    tag_categories: TagCategoryRepository
    tags: TagRepository
    course_tags: CourseTagRepository

    def commit(self) -> None:
        ...

    def rollback(self) -> None:
        ...

    def flush(self) -> None:
        ...

    def refresh(self, entity: object) -> None:
        ...