from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import CourseStatus



class MyCoursesParams(BaseModel):
    model_config = ConfigDict(extra="forbid")

    page: int = Field(default=1, ge=1)
    page_size: int = Field(
        default=16,
        ge=1,
        le=100,
    )
    status: CourseStatus | None = None