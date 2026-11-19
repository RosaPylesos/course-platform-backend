from pydantic import BaseModel, Field, ConfigDict



class TopicListParams(BaseModel):
    model_config = ConfigDict(extra="forbid")

    page: int = Field(default=1, ge=1)
    page_size: int = Field(
        default=20,
        ge=1,
        le=100,
    )