from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class UserTopicCreate(BaseModel):
    topic_id: UUID

class UserInterestResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    parent_id: UUID | None

    model_config = ConfigDict(from_attributes=True)