from app.application.tags.views import TagListView

from app.models.tag_category import TagCategory
from app.models.tag import Tag

from app.schemas.tag_category import TagCategoryListResponse
from app.schemas.tag import TagListResponse, TagResponse

def to_tag_categories_list_response(
    items: list[TagCategory],
    total: int,
    page: int,
    page_size: int,
) -> TagCategoryListResponse:

    return TagCategoryListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
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