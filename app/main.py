from typing import Any
from fastapi import FastAPI, APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.schemas.teacher import TeacherCreate
from app.api.api_v1.api import api_router
from app.core.config import settings


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

root_router = APIRouter()

@root_router.get("/", status_code=200)
def root(
        request: Request,
        db: Session = Depends(deps.get_db),
) -> dict:
    """
    Root GET
    """
    return {"msg": "hello world"}

app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)
