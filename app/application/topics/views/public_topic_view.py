from dataclasses import dataclass, field
from uuid import UUID



@dataclass(frozen=True)
class PublicTopicView:
    id: UUID
    name: str
    slug: str
    children: list["PublicTopicView"] = field(
        default_factory=list,
    )