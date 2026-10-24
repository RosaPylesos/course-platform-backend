from uuid import UUID

from app.application.exceptions import ResourceNotFoundError
from app.application.lessons.access_policy import LessonAccessPolicy
from app.application.unit_of_work import UnitOfWork

from app.models.lesson import Lesson
from app.models.user import User



class GetLessonQuery:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow
        self.access_policy = LessonAccessPolicy(uow)

    def execute(
        self,
        course_id: UUID,
        lesson_id: UUID,
        user: User,
    ) -> Lesson:
        
        self.access_policy.check_course_access(course_id,user)

        lesson = self.uow.lessons.get_by_id_for_course(
            lesson_id=lesson_id,
            course_id=course_id,
        )

        if lesson is None:
            raise ResourceNotFoundError("Lesson not found")

        return lesson