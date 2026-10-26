import uuid
from sqlalchemy import String, Enum as SQLAlchemyEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.models.enums import UserRole

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    name: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    surname: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
    )

    email: Mapped[str] = mapped_column(
        String(128),
        unique=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        nullable=False
    )

    role: Mapped[UserRole] = mapped_column(
        SQLAlchemyEnum(
            UserRole, 
            name="user_role"
        ),
        default=UserRole.STUDENT,
        nullable=False,
    )

    courses: Mapped[list["Course"]] = relationship(
        back_populates="author",
    )

    user_topics: Mapped[list["UserTopic"]] = relationship(
        back_populates="user",
    )

    enrollments: Mapped[list["Enrollment"]] = relationship(
        back_populates="user",
    )