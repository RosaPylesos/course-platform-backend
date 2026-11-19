from sqlalchemy import select

from app.database.connection import SessionLocal
from app.models.user import User
from app.models.course import Course
from app.models.topic import Topic
from app.models.enums import UserRole, CourseDifficulty, CourseStatus


def test_user_course_relationships():
    with SessionLocal() as session:
        try:
            # Создаём тему
            topic = Topic(
                name="Test topic",
                slug="test-topic",
            )
            session.add(topic)

            # Создаём автора
            user = User(
                name="Test",
                surname="Author",
                email="relationship-test@example.com",
                password_hash="temporary-test-hash",
                role=UserRole.AUTHOR,
            )
            session.add(user)
            session.flush()

            # Создаём курс, связанный с автором
            course = Course(
                author_id=user.id,
                topic_id=topic.id,
                name="Test course",
                difficulty=CourseDifficulty.BEGINNER,
                status=CourseStatus.DRAFT,
            )
            session.add(course)
            session.flush()

            # Проверяем Course -> User
            assert course.author.id == user.id
            print("Course author:", course.author.name)

            # Проверяем User -> Courses
            assert any(
                item.id == course.id for item in user.courses
            )
            print("User courses:", [item.name for item in user.courses])

            session.rollback()
            print("Relationship test passed!")

        except Exception:
            session.rollback()
            raise


if __name__ == "__main__":
    test_user_course_relationships()