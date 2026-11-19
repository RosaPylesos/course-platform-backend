from uuid import UUID

from sqlalchemy import select, asc, func, desc
from sqlalchemy.orm import Session, selectinload

from app.application.users.repository import UserRepository
from app.application.users.views import AllUsersView

from app.models.user import User
from app.models.user_topic import UserTopic
from app.models.enums import SortBy, SortOrder



class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(
        self,
        user_id: UUID,
    ) -> User | None:

        return self.db.get(User, user_id)

    def get_profile_by_id(
        self,
        user_id: UUID,
    ) -> User | None:

        statement = (
            select(User)
            .where(User.id == user_id)
            .options(
                selectinload(User.user_topics).selectinload(
                    UserTopic.topic
                )
            )
        )

        return self.db.scalar(statement)

    def get_by_email(
        self,
        email: str,
    ) -> User | None:

        statement = select(User).where(User.email == email)
        return self.db.scalar(statement)

    def list(
        self,
        page: int,
        page_size: int,
        sort_by: SortBy,
        sort_order: SortOrder,
    ) -> AllUsersView:

        sort_columns = {
            SortBy.CREATED_AT: User.created_at,
            SortBy.UPDATED_AT: User.updated_at,
        }
        sort_column = sort_columns[sort_by]

        order_column = (
            asc(sort_column)
            if sort_order == SortOrder.ASC
            else desc(sort_column)
        )

        total = self.db.scalar(
            select(func.count()).select_from(User)
        ) or 0

        statement = (
            select(User)
            .order_by(order_column, User.id)
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        items = list(self.db.scalars(statement).all())

        return AllUsersView(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=(total + page_size - 1) // page_size,
        )

    def add(
        self,
        user: User,
    ) -> None:

        self.db.add(user)