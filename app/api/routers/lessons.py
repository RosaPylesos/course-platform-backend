from uuid import UUID

from fastapi import APIRouter, status

from app.api.dependencies import (
    Db_Session, 
    Author_Or_Admin_User, 
    Current_User,
)
from app.api.mappers.lesson_mapper import (
    to_lesson_list_item_response,
)

from app.application.lessons.queries import (
    GetLessonQuery,
    GetLessonsQuery,
)
from app.application.lessons.commands import (
    CreateLessonCommand,
    UpdateLessonCommand,
    DeleteLessonCommand,
    StartLessonCommand,
    CompleteLessonCommand,
    ReorderLessonsCommand,
)
from app.application.events.setup import event_dispatcher

from app.infrastructure.unit_of_work import SqlAlchemyUnitOfWork

from app.models.lesson import Lesson

from app.schemas.lesson import (
    LessonCreate, 
    LessonResponse, 
    LessonUpdate,
    LessonReorder,
    LessonListItemResponse,
)
from app.schemas.lesson_progress import LessonProgressResponse

router = APIRouter (
    prefix="/courses/{course_id}/lessons", 
    tags=["Lessons"]
)

@router.get(
    "/",
    response_model=list[LessonListItemResponse],
    status_code=status.HTTP_200_OK,
)
def get_lessons(
    course_id: UUID,
    current_user: Current_User,
    db: Db_Session,
) -> list[LessonListItemResponse]:
    
    lessons = GetLessonsQuery(
        SqlAlchemyUnitOfWork(db)
    ).execute(
        course_id=course_id,
        user=current_user,
    )

    return [
        to_lesson_list_item_response(lesson)
        for lesson in lessons
    ]

@router.get(
    "/{lesson_id}", 
    response_model=LessonResponse,
    status_code=status.HTTP_200_OK,
)
def get_lesson(
    course_id: UUID,
    lesson_id: UUID,
    current_user: Current_User,
    db: Db_Session,
) -> Lesson:
    
    query = GetLessonQuery(SqlAlchemyUnitOfWork(db))
    return query.execute(
        course_id=course_id,
        lesson_id=lesson_id,
        user=current_user,
    )

@router.post(
    "/{lesson_id}/start",
    response_model=LessonProgressResponse,
    status_code=status.HTTP_200_OK,
)
def start_lesson(
    course_id: UUID,
    lesson_id: UUID,
    current_user: Current_User,
    db: Db_Session,
) -> LessonProgressResponse:

    command = StartLessonCommand(
        SqlAlchemyUnitOfWork(db)
    )
    return command.execute(
        course_id=course_id,
        lesson_id=lesson_id,
        user=current_user,
    )

@router.patch(
    "/{lesson_id}/complete",
    response_model=LessonProgressResponse,
    status_code=status.HTTP_200_OK,
)
def complete_lesson(
    course_id: UUID,
    lesson_id: UUID,
    current_user: Current_User,
    db: Db_Session,
) -> LessonProgressResponse:

    command = CompleteLessonCommand(
        SqlAlchemyUnitOfWork(db),
        event_dispatcher
    )
    return command.execute(
        course_id=course_id,
        lesson_id=lesson_id,
        user=current_user,
    )

@router.post(
    "/", 
    response_model=LessonResponse, 
    status_code=status.HTTP_201_CREATED,
)
def create_lesson(
    course_id: UUID,
    lesson_data: LessonCreate,
    current_user: Author_Or_Admin_User,
    db: Db_Session,
) -> Lesson:

    command = CreateLessonCommand(
        SqlAlchemyUnitOfWork(db)
    )
    return command.execute(
        course_id=course_id,
        lesson_data=lesson_data,
        user=current_user,
    )

@router.patch(
    "/reorder",
    status_code=status.HTTP_204_NO_CONTENT,
)
def reorder_lessons(
    course_id: UUID,
    reorder_data: LessonReorder,
    current_user: Author_Or_Admin_User,
    db: Db_Session,
) -> None:
    command = ReorderLessonsCommand(
        SqlAlchemyUnitOfWork(db)
    )
    command.execute(
        course_id=course_id,
        lesson_ids=reorder_data.lesson_ids,
        user=current_user,
    )

@router.patch(
    "/{lesson_id}", 
    response_model=LessonResponse,
    status_code=status.HTTP_200_OK,
)
def update_lesson(
    course_id: UUID,
    lesson_id: UUID,
    lesson_data: LessonUpdate,
    current_user: Author_Or_Admin_User,
    db: Db_Session,
) -> Lesson:
    
    command = UpdateLessonCommand(
        SqlAlchemyUnitOfWork(db)
    )
    return command.execute(
        course_id=course_id,
        lesson_id=lesson_id,
        lesson_data=lesson_data,
        user=current_user,
    )

@router.delete(
    "/{lesson_id}", 
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_lesson(
    course_id: UUID,
    lesson_id: UUID,
    current_user: Author_Or_Admin_User,
    db: Db_Session,
) -> None:

    command = DeleteLessonCommand(
        SqlAlchemyUnitOfWork(db)
    )

    command.execute(
        course_id=course_id,
        lesson_id=lesson_id,
        user=current_user,
    )