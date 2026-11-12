from uuid import UUID
from pydantic import BaseModel, ConfigDict

from app.schemas.course import CourseListItemResponse



class HomePageTopicResponse(BaseModel):
    id: UUID
    parent_id: UUID | None
    name: str
    slug: str
    has_children: bool



class HomePageSectionResponse(BaseModel):
    topic: HomePageTopicResponse
    courses: list[CourseListItemResponse]

    model_config = ConfigDict(from_attributes=True)

class HomePageResponse(BaseModel):
    sections: list[HomePageSectionResponse]

    model_config = ConfigDict(from_attributes=True)