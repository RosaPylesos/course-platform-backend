from app.database.connection import SessionLocal
from app.models.user import User
from app.models.topic import Topic
from app.models.enums import UserRole


def seed_data() -> None:
    with SessionLocal() as db:
        try:
            user = db.query(User).filter_by(
                email="test-author@example.com"
            ).first()

            if user is None:
                user = User(
                    name="Test",
                    surname="Author",
                    email="test-author@example.com",
                    password_hash="temporary-test-hash",
                    role=UserRole.AUTHOR,
                )
                db.add(user)

            topic = db.query(Topic).filter_by(
                slug="programming"
            ).first()

            if topic is None:
                topic = Topic(
                    name="Программирование",
                    slug="programming",
                )
                db.add(topic)

            db.commit()
            db.refresh(user)
            db.refresh(topic)

            print(f"Test author ID: {user.id}")
            print(f"Programming topic ID: {topic.id}")

        except Exception:
            db.rollback()
            raise


if __name__ == "__main__":
    seed_data()