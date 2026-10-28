from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.application.users.repository import UserRepository

from app.models.user import User



class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(
        self,
        user_id: UUID,
    ) -> User | None:

        return self.db.get(User, user_id)

    def get_by_email(
        self,
        email: str,
    ) -> User | None:

        statement = select(User).where(User.email == email)
        return self.db.scalar(statement)

    def list_all(self) -> list[User]:

        statement = select(User).order_by(
            User.created_at, 
            User.id,
        )
        return list(self.db.scalars(statement).all())

    def add(
        self,
        user: User,
    ) -> None:

        self.db.add(user)