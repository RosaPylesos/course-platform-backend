import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

class LessonProgress(Base, TimestampMixin):
    __tablename__ = "lesson_progress"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    enrollment_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "enrollments.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    lesson_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "lessons.id",
            ondelete="CASCADE"
        ),
        nullable=False,
    )

    is_completed: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "enrollment_id",
            "lesson_id",
            name="uq_lesson_progress_enrollment_lesson",
        ),
    )

    enrollment: Mapped["Enrollment"] = relationship(
        back_populates="lesson_progress",
    )

    lesson: Mapped["Lesson"] = relationship(
        back_populates="lesson_progress",
    )