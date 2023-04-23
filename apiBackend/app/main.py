from fastapi import FastAPI, APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
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

@root_router.get("/test", status_code=200)
def test(db: Session = Depends(deps.get_db)):
    # TODO: change /models structure. Add them to __init__.py
    return crud.student.get_multi(db=db)

# app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
