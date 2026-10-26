import uuid

from sqlalchemy import (
    String,
    Text,
    ForeignKey,
    Enum as SQLAlchemyEnum
)

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.associationproxy import association_proxy

from app.models.base import Base, TimestampMixin
from app.models.enums import CourseDifficulty, CourseStatus

class Course(Base, TimestampMixin):
    __tablename__ = "courses"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    author_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    topic_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("topics.id"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    difficulty: Mapped[CourseDifficulty] = mapped_column(
        SQLAlchemyEnum(
            CourseDifficulty,
            name="course_difficulty",
        ),
        nullable=False,
    )

    status: Mapped[CourseStatus] = mapped_column(
        SQLAlchemyEnum(
            CourseStatus,
            name="course_status",
        ),
        default=CourseStatus.DRAFT,
        nullable=False,
    )

    thumbnail_path: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    author: Mapped["User"] = relationship(
        back_populates="courses"
    )

    topic: Mapped["Topic"] = relationship(
        back_populates="courses",
    )

    course_tags: Mapped[list["CourseTag"]] = relationship(
        back_populates="course",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    enrollments: Mapped[list["Enrollment"]] = relationship(
        back_populates="course",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    lessons: Mapped[list["Lesson"]] = relationship(
        back_populates="course",
        order_by="Lesson.position",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    tags = association_proxy(
        "course_tags",
        "tag",
    )