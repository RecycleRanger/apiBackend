from typing import Any, Callable

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session

from app.api import deps
from app import schemas
from app.models.student import Student
from app.models.waste import Waste
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
        current_user: CurrentUsr = Depends(deps.get_user),
) -> Any:
    """
    Update students password
    """

    if current_user.type == UsrType.teacher:
        match crud.student.get(db=db, id=student_id):
            case Ok(v): student: Student = v
            case Err(e): raise e.httpError() from e
        if current_user.user.id == student.class_id:
            crud.student.update_password(db=db, student_id=student_id, newPassword=newPassword)
            return crud.student.get(db=db, id=student_id) \
                               .unwrap()

        raise credential_error("You don't have access to this student")
    elif current_user.type == UsrType.student:
        student_id = current_user.user.id
        crud.student.update_password(db=db, student_id=student_id, newPassword=newPassword)
        return crud.student.get(db=db, id=student_id) \
                           .unwrap()

    raise credential_error("You don't have access to this information. Please log in.")

@router.patch("/update_name")
async def update_student_name(
        newName: str,
        student_id: int = 1,
        db: Session = Depends(deps.get_db),
        current_user: CurrentUsr = Depends(deps.get_user),
) -> Any:
    """
    Update students name
    """

    if current_user.type == UsrType.teacher:
        match crud.student.get(db=db, id=student_id):
            case Ok(v): student: Student = v
            case Err(e): raise e.httpError() from e
        if current_user.user.id == student.class_id:
            crud.student.update_name(db=db, student_id=student_id, newName=newName)
            return crud.student.get(db=db, id=student_id) \
                               .unwrap()

        raise credential_error("You don't have access to this student")
    elif current_user.type == UsrType.student:
        student_id = current_user.user.id
        crud.student.update_name(db=db, student_id=student_id, newName=newName)
        return crud.student.get(db=db, id=student_id) \
                           .unwrap()

    raise credential_error("You don't have access to this information. Please log in.")

@router.patch("/update_score")
async def update_student_score(
        newScore: int,
        student_id: int = 1,
        db: Session = Depends(deps.get_db),
        current_user: CurrentUsr = Depends(deps.get_user),
) -> Any:
    """
    Update students score
    """

    if current_user.type == UsrType.teacher:
        match crud.student.get(db=db, id=student_id):
            case Ok(v):
                student: Student = v
            case Err(e):
                raise e.httpError() from e
        if current_user.user.id == student.class_id:
            crud.student.update_score(db=db, student_id=student_id, newScore=newScore)
            return crud.student.get(db=db, id=student_id) \
                               .unwrap()

        raise credential_error("You don't have access to this student")
    elif current_user.type == UsrType.student:
        student_id = current_user.user.id
        crud.student.update_score(db=db, student_id=student_id, newScore=newScore)
        return crud.student.get(db=db, id=student_id) \
                           .unwrap()

    raise credential_error("You don't have access to this information. Please log in.")

@router.get("/waste", response_model=list[schemas.Waste])
async def get_student_waste(
        student_id: int = 0,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(deps.get_db),
        current_user: CurrentUsr = Depends(deps.get_user),
) -> list[Waste]:
    """
    Get student's Waste
    """

    if current_user.type == UsrType.teacher:
        if student_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Student_id passed is invalid"
            )
        match crud.waste.get_all(
            db=db,
            student_id=student_id,
            skip=skip,
            limit=limit
        ):
            case Ok(v):
                return v
            case Err(e):
                raise e.httpError() from e
    elif current_user.type == UsrType.student:
        match crud.waste.get_all(
            db=db,
            student_id=current_user.user.id,
            skip=skip,
            limit=limit
        ):
            case Ok(v):
                return v
            case Err(e):
                raise e.httpError() from e
    raise credential_error("You don't have access to this information. Please log in.")

@router.post("/{student_id}/add_waste", response_model=schemas.Waste, status_code=201)
async def add_waste(
        student_id: int,
        *,
        db: Session = Depends(deps.get_db),
        current_usr: CurrentUsr = Depends(deps.get_user),
        waste_in: schemas.WasteCreate,
) -> Waste:
    """
    Add new Waste to the database
    """

    if waste_in.student_id != student_id:
        raise credential_error("student_id and waste_in.student_id don't match")

    if current_usr.type == UsrType.teacher or current_usr.type == UsrType.student:
        crud.student.update_numOfTrash(db=db, student_id=student_id)
        return crud.waste.create(db=db, obj_in=waste_in)

    raise credential_error("You are not authorized to make this action")
