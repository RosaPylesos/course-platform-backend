from uuid import UUID

from app.application.lessons.access_policy import LessonAccessPolicy
from app.application.unit_of_work import UnitOfWork

from app.models.lesson import Lesson
from app.models.user import User



class GetLessonsQuery:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow
        self.access_policy = LessonAccessPolicy(uow)

    def execute(
        self,
        course_id: UUID,
        user: User
    ) -> list[Lesson]:
        
        self.access_policy.check_course_access(course_id,user)
        return self.uow.lessons.list_by_course(course_id)