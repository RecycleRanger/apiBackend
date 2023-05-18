from fastapi import APIRouter

# from app.api.api_v1.endpoints import auth, students, classes
from app.api.api_v1.endpoints import auth

api_router = APIRouter()
# api_router.include_router(students.router, prefix="", tags=[""])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
