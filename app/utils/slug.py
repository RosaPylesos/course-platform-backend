from uuid import UUID
from typing import Callable
from slugify import slugify

def generate_slug(value: str) -> str:
    return slugify(value, lowercase=True)

def generate_unique_slug(
    name: str,
    slug_exists: Callable[..., bool],
    exclude_id: UUID | None = None,
) -> str:

    base_slug = generate_slug(name)
    slug = base_slug
    counter = 2

    while slug_exists(
        slug, 
        exclude_id=exclude_id,
    ):
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug