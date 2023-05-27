from typing import Any, Union, Callable

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from app.api import deps
from app.crud import student
from app.models.teacher import Teacher
from app.models.student import Student
from app import schemas
from app.core.types import UsrType


router = APIRouter()

@router.get("/{teacher_id}")
def get_class(
        teacher_id: int,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(deps.get_db),
        current_user = Depends(deps.get_user)
) -> Any:
    """
    Get all the Students of a class
    """
    credential_error: Callable[[str], Any] = lambda msg: HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=msg,
    )

    if current_user.get("type") == "teacher":
        user = schemas.Teacher(**(current_user.get("user")))
        if user.id == teacher_id:
            return student.get_class(
                db=db,
                class_id=teacher_id,
                skip=skip,
                limit=limit,
            )
        else:
            raise credential_error("You are trying to access a class that doesn't belong to you.")

    elif current_user.get("type") == "student":
        user = schemas.Student(**(current_user.get("user")))
        if user.class_id == teacher_id:
            return student.get_class_cens(
                db=db,
                class_id=teacher_id,
                skip=skip,
                limit=limit,
            )
        else:
            raise credential_error("You are trying to access a class you are not a member of.")
    raise credential_error("You don't have access to this information. Please log in.")
