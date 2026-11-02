from fastapi import FastAPI
import logging

#ROUTERS
from app.api.routers.courses import router as courses_router
from app.api.routers.lessons import router as lessons_router
from app.api.routers.topics import router as topics_router
from app.api.routers.users import router as users_router
from app.api.routers.enrollments import router as enrollments_router
from app.api.routers.tag_categories import router as tag_categories_router
from app.api.routers.tags import router as tags_router
from app.api.routers.user_topics import router as user_topics_router
from app.api.routers.home_page import router as home_page_router
from app.api.routers.admin import router as admin_router

#EXCEPTIONS AND HANDLERS
from app.api.exception_handlers import (
    business_rule_handler,
    conflict_handler,
    resource_not_found_handler,
    access_denied_handler,
    invalid_input_handler,
    invalid_credentials_handler,
)
from app.application.exceptions import (
    BusinessRuleError,
    ConflictError,
    ResourceNotFoundError,
    AccessDeniedError,
    InvalidInputError,
    InvalidCredentialsError,
)

from app.database.connection import test_connection

app = FastAPI(title="Course Platform API")

logging.basicConfig(level=logging.INFO)

app.add_exception_handler(
    ResourceNotFoundError,
    resource_not_found_handler,
)
app.add_exception_handler(
    BusinessRuleError,
    business_rule_handler,
)
app.add_exception_handler(
    ConflictError,
    conflict_handler,
)
app.add_exception_handler(
    AccessDeniedError,
    access_denied_handler,
)
app.add_exception_handler(
    InvalidInputError,
    invalid_input_handler,
)
app.add_exception_handler(
    InvalidCredentialsError,
    invalid_credentials_handler,
)

# temporary function to test pg connection
@app.on_event("startup")
def startup():
    test_connection()

@app.get("/")
def root():
    return {"message": "Course Platform API is running"}

app.include_router(home_page_router)
app.include_router(users_router)
app.include_router(admin_router)
app.include_router(courses_router)
app.include_router(lessons_router)
app.include_router(enrollments_router)
app.include_router(topics_router)
app.include_router(tag_categories_router)
app.include_router(tags_router)
app.include_router(user_topics_router)