from uuid import UUID

from app.application.courses.repository import CourseRepository
from app.application.courses.views import HomePageSectionView
from app.application.user_topics.repository import UserTopicRepository



class GetHomePageQuery:
    def __init__(
        self, 
        course_repository: CourseRepository,
        user_topic_repository: UserTopicRepository,
    ) -> None:
        self.course_repository = course_repository
        self.user_topic_repository = user_topic_repository

    def execute(
        self,
        user_id: UUID | None = None,
    ) -> list[HomePageSectionView]:

        preferred_topics = []

        if user_id is not None:
            preferred_topics = self.user_topic_repository.list_by_user(
                user_id
            )

        preferred_topic_ids = [
            topic.id for topic in preferred_topics
        ]

        sections = self.course_repository.get_home_page_sections(
            preferred_topic_ids=preferred_topic_ids,
            limit_topics=5,
            courses_per_topic=5,
        )
        return sections[:5]