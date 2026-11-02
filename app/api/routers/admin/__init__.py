from fastapi import APIRouter

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
)


router.include_router(users.router)

router.include_router(courses.router)
router.include_router(lessons.router)

router.include_router(topics.router)
router.include_router(tag_categories.router)
router.include_router(tags.router)