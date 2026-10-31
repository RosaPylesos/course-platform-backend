from app.models.lesson import Lesson

from app.schemas.lesson import LessonListItemResponse



def to_lesson_list_item_response(
    lesson: Lesson,
) -> LessonListItemResponse:
    
    return LessonListItemResponse(
        id=lesson.id,
        name=lesson.name,
        description=lesson.description,
        position=lesson.position,
    )