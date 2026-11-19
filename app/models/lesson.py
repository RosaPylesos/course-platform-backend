import uuid

from sqlalchemy import (
    ForeignKey, 
    String, 
    Text, 
    Integer,
    UniqueConstraint,
    CheckConstraint
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

class Lesson(Base, TimestampMixin):
    __tablename__ = "lessons"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    course_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "courses.id",
            ondelete="CASCADE"
        ),
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

    content: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )

    position: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "course_id",
            "position",
            name="uq_lessons_course_position",
        ),
        CheckConstraint(
            "position >= 1",
            name="ck_lessons_position_non_negative",
        ),
    )

    course: Mapped["Course"] = relationship(
        back_populates="lessons",
    )

    lesson_progress: Mapped[list["LessonProgress"]] = relationship(
        back_populates="lesson",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )