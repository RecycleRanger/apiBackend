from typing import Any
from fastapi import FastAPI, APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.schemas.teacher import TeacherCreate
# from app.api.api_v1 import api_router
from app.core.config import settings


root_router = APIRouter()
app = FastAPI(title="RecycleRanger", openapi_url=f"{settings.API_V1_STR}/openapi.json")

@root_router.get("/", status_code=200)
def root(
        request: Request,
        db: Session = Depends(deps.get_db),
) -> dict:
    """
    Root GET
    """
    return {"msg": "hello world"}

@root_router.get("/test/{class_id}", status_code=200)
def test(class_id: int, db: Session = Depends(deps.get_db)):
    return crud.student.get_class_cens(db=db, class_id=class_id)

@root_router.post("/test/createteacher", response_model=schemas.Teacher)
def create_teacher(
        *,
        db: Session = Depends(deps.get_db),
        teacher_in: TeacherCreate,
) -> Any:
    teacher = crud.teacher.create(db=db, obj_in=teacher_in)
    return teacher

# app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
