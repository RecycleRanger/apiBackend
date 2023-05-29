from typing import Any, Callable

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session

from app.api import deps
from app.models.student import Student
from app.core.myTypes import UsrType, CurrentUsr
from app import crud
from app.core.myError import Ok, Err


router = APIRouter()

credential_error: Callable[[str], Any] = lambda msg: HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=msg,
)

@router.patch("/update_password")
async def update_student_password(
        newPassword: str,
        student_id: int = 1,
        db: Session = Depends(deps.get_db),
        current_user: CurrentUsr = Depends(deps.get_current_user),
) -> Any:
    """
    Update students password
    """

    if current_user.type == UsrType.teacher:
        match crud.student.get(db=db, id=student_id):
            case Ok(v): student: Student = v
            case Err(e): raise e
        if current_user.user.id == student.class_id:
            crud.student.update_password(db=db, student_id=student_id, newPassword=newPassword)
        raise credential_error("You don't have access to this student")
    elif current_user.type == UsrType.student:
        crud.student.update_password(db=db, student_id=current_user.user.id, newPassword=newPassword)
    raise credential_error("You don't have access to this information. Please log in.")

@router.patch("/update_name")
async def update_student_name(
        newName: str,
        student_id: int = 1,
        db: Session = Depends(deps.get_db),
        current_user: CurrentUsr = Depends(deps.get_current_user),
) -> Any:
    """
    Update students name
    """

    if current_user.type == UsrType.teacher:
        match crud.student.get(db=db, id=student_id):
            case Ok(v): student: Student = v
            case Err(e): raise e
        if current_user.user.id == student.class_id:
            crud.student.update_name(db=db, student_id=student_id, newName=newName)
        raise credential_error("You don't have access to this student")
    elif current_user.type == UsrType.student:
        crud.student.update_name(db=db, student_id=student_id, newName=newName)
    raise credential_error("You don't have access to this information. Please log in.")

@router.patch("/update_score")
async def update_student_score(
        newScore: int,
        student_id: int = 1,
        db: Session = Depends(deps.get_db),
        current_user: CurrentUsr = Depends(deps.get_current_user),
) -> Any:
    """
    Update students score
    """

    if current_user.type == UsrType.teacher:
        match crud.student.get(db=db, id=student_id):
            case Ok(v): student: Student = v
            case Err(e): raise e
        if current_user.user.id == student.class_id:
            crud.student.update_score(db=db, student_id=student_id, newScore=newScore)
        raise credential_error("You don't have access to this student")
    elif current_user.type == UsrType.student:
        crud.student.update_score(db=db, student_id=student_id, newScore=newScore)
    raise credential_error("You don't have access to this information. Please log in.")
