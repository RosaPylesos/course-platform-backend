import uuid
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

class Topic(Base):
    __tablename__ = "topics"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    parent_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("topics.id"),
        nullable=True,
    )

    name: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    slug: Mapped[str] = mapped_column(
        String(128),
        unique=True,
        nullable=False,
    )

    courses: Mapped[list["Course"]] = relationship(
        back_populates="topic",
    )

    parent: Mapped["Topic | None"] = relationship(
        back_populates="children",
        remote_side="Topic.id",
    )

    children: Mapped[list["Topic"]] = relationship(
        back_populates="parent",
    )

    user_topics: Mapped[list["UserTopic"]] = relationship(
        back_populates="topic",
    )