from fastapi import APIRouter, Depends

from app.api.dependencies import require_roles
from app.models.enums import UserRole

from app.api.routers.admin import (
    courses,
    lessons,
    topics,
    tags,
    tag_categories,
    users,
)
router = APIRouter(
    prefix="/admin",
    dependencies=[Depends(require_roles(UserRole.ADMIN))],
)


router.include_router(users.router)

router.include_router(courses.router)
router.include_router(lessons.router)

router.include_router(topics.router)
router.include_router(tag_categories.router)
router.include_router(tags.router)