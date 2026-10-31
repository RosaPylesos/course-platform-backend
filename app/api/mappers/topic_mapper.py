from app.models.topic import Topic

from app.schemas.topic import TopicListResponse



def to_topics_list_response(
    items: list[Topic],
    total: int,
    page: int,
    page_size: int,
) -> TopicListResponse:

    return TopicListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=(total + page_size - 1) // page_size
    )