import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

class TagCategory(Base):
    __tablename__ = "tag_categories"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
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
    # String(64) name
    # String(128) slug

    # UNIQUE(slug)