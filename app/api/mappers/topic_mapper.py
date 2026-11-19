from app.application.topics.views import TopicListView

from app.models.topic import Topic

from app.schemas.topic import TopicListResponse, TopicResponse



def to_topics_list_response(
    view: TopicListView,
) -> TopicListResponse:

    return TopicListResponse(
        items=[
            TopicResponse.model_validate(item)
            for item in view.items
        ],
        total=view.total,
        page=view.page,
        page_size=view.page_size,
        total_pages=view.total_pages,
    )