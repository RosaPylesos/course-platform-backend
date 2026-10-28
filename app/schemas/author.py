from uuid import UUID

from pydantic import BaseModel, ConfigDict



class CourseAuthorResponse(BaseModel):
    id: UUID
    name: str
    surname: str | None

    model_config = ConfigDict(from_attributes=True)