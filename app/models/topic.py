import uuid
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

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

    # UUID id PK
    # UUID parent_id FK
    # String(64) name
    # String(128) slug

    # UNIQUE(slug)