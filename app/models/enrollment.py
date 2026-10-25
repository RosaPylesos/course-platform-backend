import uuid

from sqlalchemy import ForeignKey, Enum as SQLAlchemyEnum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.models.enums import EnrollmentStatus

class Enrollment(Base, TimestampMixin):
    __tablename__ = "enrollments"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    course_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "courses.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    status: Mapped[EnrollmentStatus] = mapped_column(
        SQLAlchemyEnum(
            EnrollmentStatus,
            name="enrollment_status",
        ),
        default=EnrollmentStatus.ACTIVE,
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "course_id",
            name="uq_enrollments_user_course",
        ),
    )

    user: Mapped["User"] = relationship(
        back_populates="enrollments",
    )

    course: Mapped["Course"] = relationship(
        back_populates="enrollments",
    )

    lesson_progress: Mapped[list["LessonProgress"]] = relationship(
        back_populates="enrollment",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    # UUID id PK
    # UUID user_id FK
    # UUID course_id FK
    # ENUM status
    # Timezone created_at
    # Timezone updated_at

    # UNIQUE(user_id, course_id)