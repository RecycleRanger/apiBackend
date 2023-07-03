from typing import Any
from fastapi import FastAPI, APIRouter, Depends, Request
from sqlalchemy.orm import Session

import logging
from fastapi import status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

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

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
	exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
	logging.error(f"{request}: {exc_str}")
	content = {'status_code': 10422, 'message': exc_str, 'data': None}
	return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

@root_router.get("/", status_code=200)
def root(
        request: Request,
        db: Session = Depends(deps.get_db),
) -> dict:
    """
    Root GET
    """
    return {"msg": "hello world"}

app.include_router(root_router)
app.include_router(api_router, prefix=settings.API_V1_STR)
