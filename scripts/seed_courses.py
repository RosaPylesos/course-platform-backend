import uuid

from app.database.connection import SessionLocal

from app.infrastructure.user_repository import SqlAlchemyUserRepository
from app.infrastructure.topic_repository import SqlAlchemyTopicRepository
from app.infrastructure.tag_repository import SqlAlchemyTagRepository

from app.models.course import Course
from app.models.course_tag import CourseTag
from app.models.lesson import Lesson
from app.models.enums import CourseStatus

from app.schemas.seed import SeedCourse, SeedData, SeedReferenceData
from app.schemas.lesson_content import LessonContent



def resolve_course_references(
    course_data: SeedCourse,
    user_repo: SqlAlchemyUserRepository,
    topic_repo: SqlAlchemyTopicRepository,
    tag_repo: SqlAlchemyTagRepository,
):
    errors = []

    author = user_repo.get_by_email(course_data.author_email)
    if author is None:
        errors.append(f"Author not found: {course_data.author_email}")

    topic = topic_repo.get_by_slug(course_data.topic_slug)
    if topic is None:
        errors.append(f"Topic not found: {course_data.topic_slug}")

    tags = []
    for slug in course_data.tag_slugs:
        tag = tag_repo.get_by_slug(slug)

        if tag is None:
            errors.append(f"Tag not found: {slug}")
        else:
            tags.append(tag)

    if errors:
        raise ValueError(
            "Failed to resolve course references:\n- "
            + "\n- ".join(errors)
        )

    return author, topic, tags

import json
from pathlib import Path

def validate_course_references(
    seed_data: SeedData,
    authors_by_email: dict,
    topics_by_slug: dict,
    tags_by_slug: dict,
) -> None:
    errors = []

    for course in seed_data.courses:
        if course.author_email not in authors_by_email:
            errors.append(
                f"Course '{course.name}': unknown author email "
                f"'{course.author_email}'"
            )

        if course.topic_slug not in topics_by_slug:
            errors.append(
                f"Course '{course.name}': unknown topic slug "
                f"'{course.topic_slug}'"
            )

        for tag_slug in course.tag_slugs:
            if tag_slug not in tags_by_slug:
                errors.append(
                    f"Course '{course.name}': unknown tag slug "
                    f"'{tag_slug}'"
                )

    if errors:
        raise ValueError(
            "Invalid references in seed data:\n- "
            + "\n- ".join(errors)
        )

BASE_DIR = Path(__file__).resolve().parent
REFERENCE_DATA_PATH = BASE_DIR / "reference_data.json"
COURSES_DATA_PATH = BASE_DIR / "courses_data.json"
IMAGE_PLACEHOLDER_URL = "https://placehold.co/1200x800"
VIDEO_PLACEHOLDER_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

def load_reference_data() -> SeedReferenceData:
    with REFERENCE_DATA_PATH.open(encoding="utf-8") as file:
        raw_data = json.load(file)

    return SeedReferenceData.model_validate(raw_data)

def build_reference_lookup(reference_data: SeedReferenceData):
    authors_by_email = {
        author.email: author
        for author in reference_data.authors
    }

    if len(authors_by_email) != len(reference_data.authors):
        raise ValueError(
            "Duplicate author emails in reference_data.json"
        )

    topics_by_slug = {}

    def collect_topics(topics):
        for topic in topics:
            topics_by_slug[topic.slug] = topic
            collect_topics(topic.children)

    collect_topics(reference_data.topics)

    def count_topics(topics):
        return sum(
            1 + count_topics(topic.children)
            for topic in topics
        )

    if len(topics_by_slug) != count_topics(reference_data.topics):
        raise ValueError(
            "Duplicate topic slugs in reference_data.json"
        )

    tags_by_slug = {
        tag.slug: tag
        for category in reference_data.tag_categories
        for tag in category.tags
    }

    total_tags = sum(
        len(category.tags)
        for category in reference_data.tag_categories
    )

    if len(tags_by_slug) != total_tags:
        raise ValueError(
            "Duplicate tag slugs in reference_data.json"
        )

    return authors_by_email, topics_by_slug, tags_by_slug

def load_courses_data() -> SeedData:
    with COURSES_DATA_PATH.open(encoding="utf-8") as file:
        raw_data = json.load(file)

    return SeedData.model_validate(raw_data)

def build_course(
    course_data,
    author,
    topic,
    tags,
) -> Course:
    course = Course(
        author=author,
        topic=topic,
        name=course_data.name,
        description=course_data.description,
        difficulty=course_data.difficulty,
        status=CourseStatus.PUBLISHED,
        thumbnail_path=None,
        course_tags=[
            CourseTag(tag=tag)
            for tag in tags
        ],
        lessons=[
            Lesson(
                name=lesson_data.name,
                description=lesson_data.description,
                position=position,
                content=build_lesson_content(lesson_data),
            )
            for position, lesson_data in enumerate(
                course_data.lessons,
                start=1,
            )
        ],
    )

    return course

def build_lesson_content(lesson_data) -> dict:
    blocks = []

    for block_data in lesson_data.content.blocks:
        block = {
            "id": uuid.uuid4(),
            "type": block_data.type,
            "content": block_data.content.model_dump(),
        }

        if block_data.type == "image":
            block["content"]["url"] = IMAGE_PLACEHOLDER_URL

        elif block_data.type == "video":
            block["content"]["url"] = VIDEO_PLACEHOLDER_URL

        blocks.append(block)

    content = LessonContent.model_validate({
        "version": 1,
        "blocks": blocks,
    })

    return content.model_dump(mode="json")

def seed_courses() -> None:
    
    reference_data = load_reference_data()

    (
        authors_by_email,
        topics_by_slug,
        tags_by_slug,
    ) = build_reference_lookup(reference_data)

    courses_data = load_courses_data()

    validate_course_references(
        courses_data,
        authors_by_email,
        topics_by_slug,
        tags_by_slug,
    )

    print("Seed data validation successful!")

    db = SessionLocal()

    try:
        user_repo = SqlAlchemyUserRepository(db)
        topic_repo = SqlAlchemyTopicRepository(db)
        tag_repo = SqlAlchemyTagRepository(db)

        courses_to_seed = []

        for course_data in courses_data.courses:
            author, topic, tags = resolve_course_references(
                course_data,
                user_repo,
                topic_repo,
                tag_repo,
            )

            course = build_course(
                course_data,
                author,
                topic,
                tags,
            )

            courses_to_seed.append(course)

        print(f"Courses prepared: {len(courses_to_seed)}")
        
        if not courses_to_seed:
            print("No courses to seed.")
        else:
            try:
                db.add_all(courses_to_seed)
                db.commit()

                print(
                    f"Successfully seeded {len(courses_to_seed)} course(s)."
                )

            except Exception:
                db.rollback()
                raise

    finally:
        db.close()

if __name__ == "__main__":
    seed_courses()