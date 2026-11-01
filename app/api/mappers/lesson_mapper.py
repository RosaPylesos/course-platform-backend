from app.models.lesson import Lesson

from app.application.lessons.views import AllLessonsView

from app.schemas.lesson import (
    LessonListItemResponse,
    ManagedLessonListItemResponse,
    ManagedLessonListResponse,
)



def to_lesson_list_item_response(
    lesson: Lesson,
) -> LessonListItemResponse:
    
    return LessonListItemResponse(
        id=lesson.id,
        name=lesson.name,
        description=lesson.description,
        position=lesson.position,
    )

def to_managed_lesson_list_response(
    view: AllLessonsView,
) -> ManagedLessonListResponse:
    
    return ManagedLessonListResponse(
        items=[
            ManagedLessonListItemResponse.model_validate(lesson)
            for lesson in view.items
        ],
        total=view.total,
        page=view.page,
        page_size=view.page_size,
        total_pages=view.total_pages,
    )