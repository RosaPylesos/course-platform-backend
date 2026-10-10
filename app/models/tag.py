import uuid

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    tag_category_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tag_categories.id"),
        nullable=False,
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
    # UUID tag_category_id FK
    # String(64) name
    # String(128) slug

    # UNIQUE(slug)