from app.models.tag_category import TagCategory
from app.models.tag import Tag

from app.schemas.tag_category import TagCategoryListResponse
from app.schemas.tag import TagListResponse

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
    items: list[Tag],
    total: int,
    page: int,
    page_size: int,
) -> TagListResponse:

    return TagListResponse (
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size,
    )