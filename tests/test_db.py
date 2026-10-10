from sqlalchemy import select

from app.database.connection import SessionLocal
from app.models.user import User
from app.models.enums import UserRole


def test_user_crud():
    with SessionLocal() as session:
        user = User(
            name="Test",
            surname=None,
            email="test-crud@example.com",
            password_hash="temporary-test-hash",
            role=UserRole.STUDENT,
        )

        try:
            # CREATE - сохраняем пользователя
            session.add(user)
            session.commit()
            session.refresh(user)

            user_id = user.id
            print(f"Created user: {user_id}")

            # READ - получаем пользователя из базы
            saved_user = session.scalar(
                select(User).where(User.id == user_id)
            )

            assert saved_user is not None
            assert saved_user.email == "test-crud@example.com"
            print(f"Read user: {saved_user.email}")

            # DELETE - удаляем тестовую запись
            session.delete(saved_user)
            session.commit()

            deleted_user = session.scalar(
                select(User).where(User.id == user_id)
            )

            assert deleted_user is None
            print("Deleted user successfully")

        except Exception:
            session.rollback()
            raise


if __name__ == "__main__":
    test_user_crud()