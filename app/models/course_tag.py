import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

class CourseTag(Base):
    __tablename__ = "course_tags"

    course_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "courses.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )

    tag_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "tags.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
    )

    course: Mapped["Course"] = relationship(
        back_populates="course_tags"
    )

    tag: Mapped["Tag"] = relationship(
        back_populates="course_tags"
    )