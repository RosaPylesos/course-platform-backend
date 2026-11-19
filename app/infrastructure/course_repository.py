from uuid import UUID

from sqlalchemy import asc, select, func, exists, desc
from sqlalchemy.orm import Session, selectinload, aliased

from app.application.courses.repository import CourseRepository
from app.application.courses.views import (
    CourseCatalogFiltersView,
    CatalogFilterTagCategoryView,
    CatalogFilterTopicView,
    CatalogFilterAuthorView,
    CatalogFilterTagView,
    CourseListItemView,
    CourseListView,
    HomePageSectionView,
    MyCoursesView,
    AllCoursesView,
    HomePageTopicView,
)

from app.models.enums import (
    CourseStatus, 
    CourseDifficulty,
    SortBy,
    SortOrder,
)
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

    def list_all(
        self,
        page: int,
        page_size: int,
        sort_by: SortBy,
        sort_order: SortOrder
    ) -> AllCoursesView:

        offset = (page - 1) * page_size

        sort_column = {
            SortBy.CREATED_AT: Course.created_at,
            SortBy.UPDATED_AT: Course.updated_at,
        }[sort_by]

        order_column = (
            asc(sort_column)
            if sort_order == SortOrder.ASC 
            else desc(sort_column)
        )

        statement = (
            select(Course)
            .order_by(order_column, Course.id)
            .offset(offset)
            .limit(page_size)
        )

        items = list(self.db.scalars(statement).all())

        total_statement = select(func.count(Course.id))
        total = self.db.scalar(total_statement) or 0

        return AllCoursesView(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=(total + page_size - 1) // page_size,
        )

    def get_home_page_sections(
        self,
        preferred_topic_ids: list[UUID] | None = None,
        limit_topics: int = 5,
        courses_per_topic: int = 5,
    ) -> list[HomePageSectionView]:

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

        child_topic = aliased(Topic)

        has_children = exists(
            select(child_topic.id).where(
                child_topic.parent_id == Topic.id
            )
        )

        # Popular + Preferred Topics
        topic_statement = (
            select(
                Topic,
                topic_counts.c.course_count,
                has_children.label("has_children"),
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
                .limit(limit_topics)
            ).all()

        remaining = limit_topics - len(preferred_topics)

        popular_topics = []
        if remaining > 0:
            popular_topics = self.db.execute(
                topic_statement
                .where(
                    Topic.id.not_in(preferred_ids)
                    if preferred_ids else True
                )
                .limit(remaining)
            ).all()

        selected_topics = preferred_topics + popular_topics

        # Course amount limitation per topic
        selected_topic_ids = [
            topic.id for topic, _, _ in selected_topics
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
        courses_by_topic: dict[UUID, list[CourseListItemView]] = {}

        for course, count in rows:
            courses_by_topic.setdefault(
                course.topic_id, []
            ).append(
                CourseListItemView(
                    course=course,
                    lesson_count=count,
                )
            )

        # returns final list of HomePageSectionView
        return [
            HomePageSectionView(
                topic=HomePageTopicView(
                    id=topic.id,
                    parent_id=topic.parent_id,
                    name=topic.name,
                    slug=topic.slug,
                    has_children=has_children,
                ),
                courses=courses_by_topic[topic.id],
            )
            for topic, _, has_children in selected_topics
            if courses_by_topic.get(topic.id)
        ]

    def list_published_for_catalog(
        self,
        page: int,
        page_size: int,
        search: str | None = None,
        author_ids: list[UUID] | None = None,
        topic_ids: list[UUID] | None = None,
        topic_id: UUID | None = None,
        include_descendants: bool = False,
        difficulties: list[CourseDifficulty] | None = None,
        tags_ids_by_category: dict[UUID, list[UUID]] | None = None,
    ) -> CourseListView:

        filters = [Course.status == CourseStatus.PUBLISHED]
        print(topic_ids)

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

        if topic_id is not None:
            if include_descendants:
                topic_tree = (
                    select(Topic.id)
                    .where(Topic.id == topic_id)
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
                    Course.topic_id == topic_id
                )

        if selected_topic_ids:
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
            CourseListItemView(
                course=course,
                lesson_count=count,
            )
            for course, count in rows
        ]

        return CourseListView(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=(total + page_size - 1) // page_size,
        )

    def get_catalog_filters(
        self,
        topic_id: UUID | None = None,
    ) -> CourseCatalogFiltersView:

        filters = [Course.status == CourseStatus.PUBLISHED]

        ### DESCENDANTS CONDITION

        context_topic_tree = None

        if topic_id is not None:
            context_topic_tree = (
                select(Topic.id.label("id"))
                .where(Topic.id == topic_id)
                .cte("context_topic_tree", recursive=True)
            )

            child_topic = aliased(Topic)

            context_topic_tree = context_topic_tree.union_all(
                select(child_topic.id.label("id"))
                .join(
                    context_topic_tree,
                    child_topic.parent_id == context_topic_tree.c.id,
                )
            )

            filters.append(
                Course.topic_id.in_(
                    select(context_topic_tree.c.id)
                )
            )

        ### AUTHORS FILTER
        authors_statement = (
            select(User)
            .join(Course, Course.author_id == User.id)
            .where(*filters)
            .distinct()
            .order_by(User.name, User.surname)
        )

        authors = [
            CatalogFilterAuthorView(
                id=author.id,
                name=author.name,
                surname=author.surname,
            )
            for author in self.db.scalars(authors_statement).all()
        ]

        ### DIFFICULTIES FILTER
        difficulties_statement = (
            select(Course.difficulty)
            .where(*filters)
            .distinct()
            .order_by(Course.difficulty)
        )

        difficulties = list (
            self.db.scalars(difficulties_statement).all()
        )

        ### TOPICS FILTER
        available_topic_tree = (
            select(Course.topic_id.label("id"))
            .where(*filters)
            .distinct()
            .cte("available_topic_tree", recursive=True)
        )

        available_topic_tree = available_topic_tree.union(
            select(Topic.parent_id.label("id"))
            .join(
                available_topic_tree,
                Topic.id == available_topic_tree.c.id,
            )
            .where(Topic.parent_id.is_not(None))
        )

        topics_statement = (
            select(Topic)
            .where(Topic.id.in_(
                select(available_topic_tree.c.id)
                )
            )
        )

        if topic_id is not None:
            topics_statement = topics_statement.where(
                Topic.id != topic_id
            )

        topics_statement = topics_statement.order_by(
            Topic.name, 
            Topic.id,
        )

        topics =[
            CatalogFilterTopicView(
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
            .where(*filters)
            .distinct()
            .order_by(Tag.name)
        )

        used_tags = self.db.scalars(used_tags_statement).all()

        ### TAGS GROUPING
        tags_by_category: dict[UUID, list[CatalogFilterTagView]] = {}

        for tag in used_tags:
            tags_by_category.setdefault(
                tag.tag_category_id, []
            ).append(
                CatalogFilterTagView(
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
                CatalogFilterTagCategoryView(
                    id=category.id,
                    name=category.name,
                    tags=tags_by_category[category.id]
                )
                for category in self.db.scalars(categories_statement).all()
            ]
        else:
            tag_categories = []

        return CourseCatalogFiltersView(
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

        base_filters = [Course.author_id == author_id]

        offset = (page - 1) * page_size

        statement = (
            select(Course)
            .where(*base_filters)
            .options(
                selectinload(Course.topic),
                selectinload(Course.course_tags).selectinload(
                    CourseTag.tag
                ),
            )
            .order_by(Course.created_at.desc(), Course.id)
            
        )

        if status is not None:
            statement = statement.where(Course.status == status)

        statement = (
            statement
            .offset(offset)
            .limit(page_size)
        )

        items = list(self.db.scalars(statement).all())

        ### Count total course amount (incl. filters)
        total_statement = (
            select(func.count(Course.id))
            .where(
                *base_filters,
                *(
                    [Course.status == status] if status is not None else []
                ),
            )
        )

        total = self.db.scalar(total_statement) or 0

        ### Count course amount per status
        counts_statement = (
            select(Course.status, func.count(Course.id))
            .where(*base_filters)
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
    ) -> CourseListItemView | None:

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

        return CourseListItemView(
            course=course,
            lesson_count=count,
        )

    def add(self, course: Course) -> None:
        self.db.add(course)

    def delete(self, course: Course) -> None:
        self.db.delete(course)