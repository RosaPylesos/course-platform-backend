from dataclasses import dataclass

from app.models.enums import SortBy, SortOrder

from app.application.lessons.views import AllLessonsView
from app.application.lessons.repository import LessonRepository



@dataclass(frozen=True)
class GetAllLessonsInput:
    page: int
    page_size: int
    sort_by: SortBy
    sort_order: SortOrder



class GetAllLessonsQuery:
    def __init__(self, lesson_repository: LessonRepository) -> None:
        self.lesson_repository = lesson_repository

    def execute(
        self,
        input: GetAllLessonsInput
    ) -> AllLessonsView:
        
        return self.lesson_repository.list_all(
            page=input.page,
            page_size=input.page_size,
            sort_by=input.sort_by,
            sort_order=input.sort_order
        )