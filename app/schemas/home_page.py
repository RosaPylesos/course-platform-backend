from pydantic import BaseModel, ConfigDict

from app.schemas.course import CourseListItemResponse
from app.schemas.topic import TopicResponse



class HomePageSectionResponse(BaseModel):
    topic: TopicResponse
    courses: list[CourseListItemResponse]

    model_config = ConfigDict(from_attributes=True)

class HomePageResponse(BaseModel):
    sections: list[HomePageSectionResponse]

    model_config = ConfigDict(from_attributes=True)