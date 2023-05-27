from typing import Generator, Optional, Any, Union
from dataclasses import dataclass

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from pydantic import BaseModel
from sqlalchemy.orm.session import Session

from app.core.myTypes import UsrType, Payload, CurrentUsr
from app.core.myError import Result, Ok, Err
from app.core.auth import teacher_oauth2_scheme, student_oauth2_scheme
from app.core.config import settings
from app.db.session import SessionLocal
from app.models.teacher import Teacher
from app.models.student import Student
from app.crud import crud_teacher
from app.crud import crud_student


class TokenData(BaseModel):
    username: Optional[str] = None


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def _get_payload(
        db: Session,
        token: str,
) -> Result[Payload, JWTError]:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )
        payload = Payload(**payload)
    except JWTError:
        return Err(JWTError("Error with payload"))
    return Ok(payload)

async def get_user(
        db: Session = Depends(get_db),
        teacher_token: str = Depends(teacher_oauth2_scheme),
        student_token: str = Depends(student_oauth2_scheme),
) -> CurrentUsr:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    match _get_payload(db, teacher_token):
        case Ok(v): 
            user_id: Optional[str] = v.sub
            type: UsrType = UsrType(v.usr)
        case Err(e):
            match _get_payload(db, student_token):
                case Ok(v):
                    user_id: Optional[str] = v.sub
                    type: UsrType = UsrType(v.usr)
                case Err(e):
                    raise credentials_exception

    if type == UsrType.teacher:
        teacher_data = crud_teacher.teacher.get(
            db=db,
            id=user_id
        )
        if teacher_data is None:
            raise credentials_exception
        return CurrentUsr(
            user=teacher_data,
            type=type
        )
    elif type == UsrType.student:
        student_data = crud_student.student.get(
            db=db,
            id=user_id
        )
        if student_data is None:
            raise credentials_exception
        return CurrentUsr(
            user=student_data,
            type=type
        )
    raise credentials_exception


# async def get_user(
#         db: Session = Depends(get_db),
#         teacher_token: str = Depends(teacher_oauth2_scheme),
#         student_token: str = Depends(student_oauth2_scheme),
# ) -> Any:

#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"}
#     )

#     try:
#         # Teacher payload
#         payload = jwt.decode(
#             teacher_token,
#             settings.JWT_SECRET,
#             algorithms=[settings.ALGORITHM],
#             options={"verify_aud": False},
#         )
#         payload = Payload(**payload)

#         user_id: Optional[str] = payload.sub
#         # TODO: Left here
#         type: UsrType = payload.usr
#         if user_id is None or type is None:
#             raise credentials_exception
#         token_data = TokenData(username=user_id)
#     except JWTError:
#         try:
#             payload = jwt.decode(
#                 student_token,
#                 settings.JWT_SECRET,
#                 algorithms=[settings.ALGORITHM],
#                 options={"verify_aud": False}
#             )
#             payload = Payload(**payload)

#             user_id: Optional[str] = payload.sub
#             type: UsrType = payload.usr
#             if user_id is None or type is None:
#                 raise credentials_exception
#             token_data = TokenData(username=user_id)
#         except JWTError:
#             raise credentials_exception

#     if type == UsrType.teacher:
#         teacher_data = crud_teacher.teacher.get(
#             db=db,
#             id=token_data.username
#         )
#         if teacher_data is None:
#             raise credentials_exception
#         return {
#             "user": teacher_data.__dict__,
#             "type": type
#         }
#     elif type == UsrType.student:
#         student_data = crud_student.student.get(
#             db=db,
#             id=token_data.username
#         )
#         if student_data is None:
#             raise credentials_exception
#         return {
#             "user": student_data.__dict__,
#             "type": type
#         }
#     raise credentials_exception

async def get_current_user(
        db: Session = Depends(get_db),
        token: str = Depends(teacher_oauth2_scheme),
) -> Teacher:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )

        username: Optional[str] = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    teacher = db.query(Teacher) \
             .filter(Teacher.id == token_data.username) \
             .first()
    if teacher is None:
        raise credentials_exception
    return teacher
