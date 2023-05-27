from fastapi import APIRouter

# from app.api.api_v1.endpoints import auth, students, classes
from app.api.api_v1.endpoints import auth, classes


api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(classes.router, prefix="/class", tags=["class"])
