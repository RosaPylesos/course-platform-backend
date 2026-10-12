from fastapi import FastAPI

#ROUTERS
from app.api.routers.courses import router as courses_router

from app.database.connection import test_connection

app = FastAPI(title="Course Platform API")

# temporary function to test pg connection
@app.on_event("startup")
def startup():
    test_connection()

@app.get("/")
def root():
    return {"message": "Course Platform API is running"}

app.include_router(courses_router)