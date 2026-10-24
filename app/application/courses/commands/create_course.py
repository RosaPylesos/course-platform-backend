from uuid import UUID

from app.application.unit_of_work import UnitOfWork

from app.models.course import Course

from app.schemas.course import CourseCreate



class CreateCourseCommand:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def execute(
        self,
        course_data: CourseCreate,
        author_id: UUID,
    ) -> Course:

        course = Course(
            **course_data.model_dump(),
            author_id=author_id,
        )

        self.uow.courses.add(course)
        self.uow.commit()
        self.uow.refresh(course)

        return course