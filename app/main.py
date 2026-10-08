from fastapi import FastAPI

from app.database.connection import test_connection

app = FastAPI(title="Course Platform API")

# temporary function to test pg connection
@app.on_event("startup")
def startup():
    test_connection()

@app.get("/")
def root():
    return {"message": "Course Platform API is running"}