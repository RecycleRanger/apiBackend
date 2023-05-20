from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from app.api import deps
from app import schemas
from app import crud
from app.core.auth import authenticate, create_access_token

from app.models.teacher import Teacher


router = APIRouter()

@router.post("/login/teacher")
def login(
        db: Session = Depends(deps.get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Get the JWT for a user with data from OAuth2 request form body.
    """

    teacher = authenticate(
        username=form_data.username,
        password=form_data.password,
        db=db
    )
    if not teacher:
        raise HTTPException(
            status_code=400,
            detail="Incorect username or password"
        )
    return {
        "access_token": create_access_token(sub=teacher.id, usr="teacher"),
        "token_type": "bearer",
    }

@router.get("/me", response_model=schemas.Teacher)
def read_users_me(
        current_user: Teacher = Depends(deps.get_current_user)
):
    """
    Fetch the current logged in user.
    """

    user = current_user
    return user

@router.post("/signup/teacher", response_model=schemas.Teacher, status_code=201)
def create_teacher_signup(
        *,
        db: Session = Depends(deps.get_db),
        teacher_in: schemas.teacher.TeacherCreate,
) -> Any:
    """
    Create new teacher with signup
    """

    teacher = db.query(Teacher) \
                .filter(Teacher.username == teacher_in.username) \
                .first()
    if teacher:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists"
        )
    teacher = crud.teacher.create(db=db, obj_in=teacher_in)

    return teacher
