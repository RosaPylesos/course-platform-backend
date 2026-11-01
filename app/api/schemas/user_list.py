from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import SortBy, SortOrder



class UserListParams(BaseModel):
    model_config = ConfigDict(extra="forbid")

    page: int = Field(default=1, ge=1)
    page_size: int = Field(
        default=20, 
        ge=1, 
        le=100
    )
    sort_by: SortBy = SortBy.CREATED_AT
    sort_order: SortOrder = SortOrder.DESC