from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, students, classes

api_router = APIRouter()
api_router.include_router(students.router, prefix="", tags=[""])
