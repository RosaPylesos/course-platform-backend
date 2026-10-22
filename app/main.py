from fastapi import FastAPI

#ROUTERS
from app.api.routers.courses import router as courses_router
from app.api.routers.lessons import router as lessons_router
from app.api.routers.topics import router as topics_router
from app.api.routers.users import router as users_router
from app.api.routers.enrollments import router as enrollment_router

#EXCEPTIONS AND HANDLERS
from app.api.exception_handlers import (
    business_rule_handler,
    conflict_handler,
    resourse_not_found_handler,
)
from app.application.exceptions import (
    BusinessRuleError,
    ConflictError,
    ResourceNotFoundError,
)

from app.database.connection import test_connection

app = FastAPI(title="Course Platform API")

app.add_exception_handler(
    ResourceNotFoundError,
    resourse_not_found_handler,
)
app.add_exception_handler(
    BusinessRuleError,
    business_rule_handler,
)
app.add_exception_handler(
    ConflictError,
    conflict_handler,
)

# temporary function to test pg connection
@app.on_event("startup")
def startup():
    test_connection()

@app.get("/")
def root():
    return {"message": "Course Platform API is running"}

app.include_router(courses_router)
app.include_router(lessons_router)
app.include_router(topics_router)
app.include_router(users_router)
app.include_router(enrollment_router)