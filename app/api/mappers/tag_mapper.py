from app.application.tags.views import TagListView
from app.application.tag_categories.views import (
    TagCategoryListView
)

from app.schemas.tag_category import (
    TagCategoryListResponse,
    TagCategoryResponse,
)
from app.schemas.tag import TagListResponse, TagResponse

def to_tag_categories_list_response(
    view: TagCategoryListView
) -> TagCategoryListResponse:

    return TagCategoryListResponse(
        items=[
            TagCategoryResponse.model_validate(category)
            for category in view.items
        ],
        total=view.total,
        page=view.page,
        page_size=view.page_size,
        total_pages=view.total_pages,
    )

def to_tag_list_response(
    view: TagListView
) -> TagListResponse:

    return TagListResponse (
        items =[
            TagResponse.model_validate(tag)
            for tag in view.items
        ],
        total=view.total,
        page=view.page,
        page_size=view.page_size,
        total_pages=view.total_pages,
    )