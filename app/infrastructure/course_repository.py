from uuid import UUID

from sqlalchemy import select, func, exists
from sqlalchemy.orm import Session, selectinload, aliased

from app.application.courses.repository import CourseRepository
from app.application.courses.views import (
    CourseCatalogFilters,
    CatalogFilterTagCategory,
    CatalogFilterTopic,
    CatalogFilterAuthor,
    CatalogFilterTag,
    CourseListItem,
    HomePageSection,
    MyCoursesView,
)

from app.models.enums import CourseStatus, CourseDifficulty
from app.models.course_tag import CourseTag
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.topic import Topic
from app.models.tag import Tag
from app.models.user import User
from app.models.tag_category import TagCategory



class SqlAlchemyCourseRepository(CourseRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_all(self) -> list[Course]:

        statement = (
            select(Course)
            .order_by(Course.created_at.desc(), Course.id)
        )
        return list(self.db.scalars(statement).all())

    def list_published(self) -> list[Course]:

        statement = select(Course).where(
            Course.status == CourseStatus.PUBLISHED
        )
        return list(self.db.scalars(statement).all())

    def get_home_page_sections(
        self,
        preferred_topic_ids: list[UUID] | None = None,
        limit_topics: int = 5,
        courses_per_topic: int = 5,
    ) -> list[HomePageSection]:

        # Topic counts
        topic_counts = (
            select(
                Course.topic_id,
                func.count(Course.id).label("course_count"),
            )
            .where(Course.status == CourseStatus.PUBLISHED)
            .group_by(Course.topic_id)
            .subquery()
        )

        # Popular + Preferred Topics
        topic_statement = (
            select(
                Topic,
                topic_counts.c.course_count,
            )
            .join(
                topic_counts,
                topic_counts.c.topic_id == Topic.id,
            )
            .order_by(
            topic_counts.c.course_count.desc(), 
            Topic.name
            )
        )

        preferred_ids = list(
            dict.fromkeys(preferred_topic_ids or [])
        )

        preferred_topics = []
        if preferred_ids:
            preferred_topics = self.db.execute(
                topic_statement
                .where(Topic.id.in_(preferred_ids))
            ).all()

        popular_topics = self.db.execute(
            topic_statement
            .where(
                Topic.id.not_in(preferred_ids)
                if preferred_ids else True
            )
            .limit(limit_topics)
        ).all()

        selected_topics = preferred_topics + popular_topics

        # Course amount limitation per topic
        selected_topic_ids = [
            topic.id for topic, _ in selected_topics
        ]

        if not selected_topic_ids:
            return []

        ranked_courses = (
            select(
                Course.id.label("course_id"),
                func.row_number()
                .over(
                    partition_by=Course.topic_id,
                    order_by=(
                        Course.created_at.desc(),
                        Course.id,
                    ),
                )
                .label("row_number"),
            )
            .where(
                Course.status == CourseStatus.PUBLISHED,
                Course.topic_id.in_(selected_topic_ids),
            )
            .subquery()
        )

        lesson_count = (
            select(func.count(Lesson.id))
            .where(Lesson.course_id == Course.id)
            .correlate(Course)
            .scalar_subquery()
        )

        course_statement = (
            select(
                Course,
                lesson_count.label("lesson_count"),
            )
            .join(
                ranked_courses,
                ranked_courses.c.course_id == Course.id,
            )
            .where(ranked_courses.c.row_number <= courses_per_topic)
            .options(
                selectinload(Course.author),
                selectinload(Course.topic),
                selectinload(Course.course_tags).selectinload(
                    CourseTag.tag
                ),
            )
            .order_by(
                Course.topic_id,
                Course.created_at.desc(), 
                Course.id
            )
        )

        rows = self.db.execute(course_statement).all()

        # Organize courses by topic
        courses_by_topic: dict[UUID, list[CourseListItem]] = {}

        for course, count in rows:
            courses_by_topic.setdefault(
                course.topic_id, []
            ).append(
                CourseListItem(
                    course=course,
                    lesson_count=count,
                )
            )

        # returns final list of HomePageSection
        return [
            HomePageSection(
                topic=topic,
                courses=courses_by_topic[topic.id],
            )
            for topic, _ in selected_topics
            if courses_by_topic.get(topic.id)
        ]

    def list_published_for_catalog(
        self,
        page: int,
        page_size: int,
        search: str | None = None,
        author_ids: list[UUID] | None = None,
        topic_ids: list[UUID] | None = None,
        include_descendants: bool = False,
        difficulties: list[CourseDifficulty] | None = None,
        tags_ids_by_category: dict[UUID, list[UUID]] | None = None,
    ) -> tuple[list[CourseListItem], int]:

        filters = [Course.status == CourseStatus.PUBLISHED]

        ### SEARCH FILTER
        if search and search.strip():
            filters.append(
                Course.name.ilike(f"%{search.strip()}%")
            )

        ### AUTHOR FILTER
        if author_ids is not None:
            filters.append(Course.author_id.in_(author_ids))

        ### DIFFICULTY FILTER
        if difficulties is not None:
            filters.append(Course.difficulty.in_(difficulties))

        ### TOPIC FILTER
        selected_topic_ids = list(topic_ids or [])

        if selected_topic_ids:
            if include_descendants:
                topic_tree = (
                    select(Topic.id)
                    .where(Topic.id.in_(selected_topic_ids))
                    .cte("topic_tree", recursive=True)
                )

                child_topic = aliased(Topic)

                topic_tree = topic_tree.union_all(
                    select(child_topic.id).join(
                        topic_tree,
                        child_topic.parent_id == topic_tree.c.id,
                    )
                )

                filters.append(
                    Course.topic_id.in_(
                        select(topic_tree.c.id)
                    )
                )
            else:
                filters.append(
                    Course.topic_id.in_(selected_topic_ids)
                )

        ### TAGS FILTERING
        for category_id, tag_ids in (
            tags_ids_by_category or {}).items():
            if not tag_ids:
                continue

            matching_tag = exists(
                select(1)
                .select_from(CourseTag)
                .join(Tag, Tag.id == CourseTag.tag_id)
                .where(
                    CourseTag.course_id == Course.id,
                    Tag.tag_category_id == category_id,
                    CourseTag.tag_id.in_(tag_ids),
                )
            )
            filters.append(matching_tag)

        ### LESSON COUNT
        lesson_count = (
            select(func.count(Lesson.id))
            .where(Lesson.course_id == Course.id)
            .correlate(Course)
            .scalar_subquery()
        )

        ### CURRENT PAGE
        statement = (
            select(Course, lesson_count.label("lesson_count"))
            .where(*filters)
            .options(
                selectinload(Course.author),
                selectinload(Course.topic),
                selectinload(Course.course_tags).selectinload(
                    CourseTag.tag
                ),
            )
            .order_by(Course.created_at.desc(), Course.id)
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        ### COURSE COUNTING W/ FILTERS
        count_statement = (
            select(func.count())
            .select_from(Course)
            .where(*filters)
        )

        rows = self.db.execute(statement).all()
        total = self.db.scalar(count_statement) or 0

        items = [
            CourseListItem(
                course=course,
                lesson_count=count,
            )
            for course, count in rows
        ]

        return items, total

    def get_catalog_filters(self) -> CourseCatalogFilters:

        published_filter = Course.status == CourseStatus.PUBLISHED

        ### AUTHORS FILTER
        authors_statement = (
            select(User)
            .join(Course, Course.author_id == User.id)
            .where(published_filter)
            .distinct()
            .order_by(User.name, User.surname)
        )

        authors = [
            CatalogFilterAuthor(
                id=author.id,
                name=author.name,
                surname=author.surname,
            )
            for author in self.db.scalars(authors_statement).all()
        ]

        ### DIFFICULTIES FILTER
        difficulties_statement = (
            select(Course.difficulty)
            .where(published_filter)
            .distinct()
            .order_by(Course.difficulty)
        )

        difficulties = list (
            self.db.scalars(difficulties_statement).all()
        )

        ### TOPICS FILTER
        used_topics_statement = (
            select(Course.topic_id)
            .where(
                published_filter,
                Course.topic_id.is_not(None),
            )
            .distinct()
        )

        used_topics_ids = set(
            self.db.scalars(used_topics_statement).all()
        )

        ## TOPICS PARENTS
        topic_ids = set(used_topics_ids)

        while used_topics_ids:
            parent_ids_statement = select(Topic.parent_id).where(
                Topic.id.in_(used_topics_ids),
                Topic.parent_id.is_not(None),
            )

            parent_ids = set(
                self.db.scalars(parent_ids_statement).all()
            )

            new_parent_ids = parent_ids - topic_ids

            if not new_parent_ids:
                break

            topic_ids.update(new_parent_ids)
            used_topics_ids = new_parent_ids

        topics_statement = (
            select(Topic)
            .where(Topic.id.in_(topic_ids))
            .order_by(Topic.name)
        )

        topics = [
            CatalogFilterTopic(
                id=topic.id,
                name=topic.name,
                parent_id=topic.parent_id,
                slug=topic.slug,
            )
            for topic in self.db.scalars(topics_statement).all()
        ]

        ### TAGS FILTER
        used_tags_statement = (
            select(Tag)
            .join(CourseTag, CourseTag.tag_id == Tag.id)
            .join(Course, Course.id == CourseTag.course_id)
            .where(Course.status == CourseStatus.PUBLISHED)
            .distinct()
            .order_by(Tag.name)
        )

        used_tags = self.db.scalars(used_tags_statement).all()

        ### TAGS GROUPING
        tags_by_category: dict[UUID, list[CatalogFilterTag]] = {}

        for tag in used_tags:
            tags_by_category.setdefault(
                tag.tag_category_id, []
            ).append(
                CatalogFilterTag(
                    id=tag.id,
                    name=tag.name,
                    slug=tag.slug,
                )
            )

        category_ids = set(tags_by_category.keys())

        if category_ids:

            categories_statement = (
                select(TagCategory)
                .where(TagCategory.id.in_(category_ids))
                .order_by(TagCategory.name)
            )

            tag_categories = [
                CatalogFilterTagCategory(
                    id=category.id,
                    name=category.name,
                    tags=tags_by_category[category.id]
                )
                for category in self.db.scalars(categories_statement).all()
            ]
        else:
            tag_categories = []

        return CourseCatalogFilters(
            authors=authors,
            topics=topics,
            tag_categories=tag_categories,
            difficulties=difficulties,
        )

    def list_by_author(
        self,
        author_id: UUID,
        page: int,
        page_size: int,
        status: CourseStatus | None = None,
    ) -> MyCoursesView:

        offset = (page - 1) * page_size

        statement = (
            select(Course)
            .where(Course.author_id == author_id)
            .options(
                selectinload(Course.topic),
                selectinload(Course.course_tags).selectinload(
                    CourseTag.tag
                ),
            )
            .order_by(Course.created_at.desc(), Course.id)
            # .offset(offset)
            # .limit(page_size)
        )

        if status is not None:
            statement = statement.where(Course.status == status)

        items = list(self.db.scalars(statement).all())

        ### Count total course amount (incl. filters)
        total_statement = (
            select(func.count(Course.id))
            .where(Course.author_id == author_id)
        )

        if status is not None:
            total_statement = total_statement.where(
                Course.status == status
            )

        total = self.db.scalar(total_statement) or 0

        ### Count course amount per status
        counts_statement = (
            select(Course.status, func.count(Course.id))
            .where(Course.author_id == author_id)
            .group_by(Course.status)
        )

        counts_rows = self.db.execute(counts_statement).all()

        status_counts = {
            course_status: count
            for course_status, count in counts_rows
        }

        for course_status in CourseStatus:
            status_counts.setdefault(course_status, 0)

        total_pages = (total + page_size - 1) // page_size

        return MyCoursesView(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            status_counts=status_counts,
        )

    def get_by_id(self, course_id: UUID) -> Course | None:
        return self.db.get(Course, course_id)

    def get_by_id_with_relations(
        self,
        course_id: UUID
    ) -> Course | None:

        statement = (
            select(Course)
            .where(Course.id == course_id)
            .options(
                selectinload(Course.topic),
                selectinload(Course.course_tags).selectinload(
                    CourseTag.tag
                ),
            )
        )

        return self.db.scalar(statement)

    def get_detail(
        self,
        course_id: UUID,
    ) -> CourseListItem | None:

        lesson_count = (
            select(func.count(Lesson.id))
            .where(Lesson.course_id == Course.id)
            .correlate(Course)
            .scalar_subquery()
        )

        statement = (
            select(
                Course, lesson_count.label("lesson_count")
            )
            .where(Course.id == course_id)
            .options(
                selectinload(Course.author),
                selectinload(Course.topic),
                selectinload(Course.course_tags).selectinload(
                    CourseTag.tag
                )
            )
        )

        row = self.db.execute(statement).one_or_none()

        if row is None:
            return None

        course, count = row

        return CourseListItem(
            course=course,
            lesson_count=count,
        )

    def add(self, course: Course) -> None:
        self.db.add(course)

    def delete(self, course: Course) -> None:
        self.db.delete(course)