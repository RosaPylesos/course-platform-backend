
from app.database.connection import SessionLocal
from app.infrastructure.unit_of_work import SqlAlchemyUnitOfWork


def main() -> None:
    db = SessionLocal()

    try:
        uow = SqlAlchemyUnitOfWork(db)

        author_email = "test-author@example.com"
        author = uow.users.get_by_email(author_email)

        if author is None:
            print(f"Author not found: {author_email}")
            return

        print(f"Author found: {author.name}")
        print(f"Email: {author.email}")
        print(f"Role: {author.role.value}")

        topic_slug = "programmirovanie"
        topic = uow.topics.get_by_slug(topic_slug)

        if topic is None:
            print(f"Topic not found: {topic_slug}")
            return

        print(f"Topic found: {topic.name}")
        print(f"Slug: {topic.slug}")

        tag = uow.tags.get_by_slug("test123")

        if tag is not None:
            print(f"Tag found: {tag.name}")
            print(f"Slug: {tag.slug}")
            print(f"Category ID: {tag.tag_category_id}")
        else:
            print("Tag not found")

    finally:
        db.close()


if __name__ == "__main__":
    main()
