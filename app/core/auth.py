from typing import Optional, MutableMapping, List, Union
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session
from jose import jwt

from app.core.myTypes import UsrType
from app.models.teacher import Teacher
from app.models.student import Student
from app import crud, schemas
from app.core.config import settings
from app.core.security import verify_password
from app.core.myError import Ok, Err


JWTPayloadMapping = MutableMapping[
    str,
    Union[datetime, bool, str, List[str], List[int]]
]

teacher_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login/teacher",
    scheme_name="teacher_oauth2_scheme"
)

student_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login/student",
    scheme_name="student_oauth2_scheme"
)

def authenticate(
        *,
        id: Optional[int] = None,
        username: Optional[str] = None,
        password: str,
        db: Session,
        usrType: UsrType,
) -> Teacher | Student | None:

    # type: ignore
    if usrType == UsrType.teacher and username:
        match crud.teacher.get_by_username(db=db, username=username):
            case Ok(v):
                user = v
            case Err(e):
                return None
    else:
        if id:
            match crud.student.get(db=db, id=int(id)):
                case Ok(v):
                    user = v
                case Err(e):
                    return None
        elif username:
            match crud.student.get_by_username(db=db, username=username):
                case Ok(v):
                    user = v
                case Err(e):
                    return None
        else:
            return None

    if not user: # type: ignore
        return None

    if not verify_password(password, str(user.hashed_password)):
        return None
    return user

def create_access_token(*, sub: str, usr: UsrType) -> str:
    return _create_token(
        token_type="access_token",
        lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
        usr=usr,
    )

def _create_token(
        token_type: str,
        lifetime: timedelta,
        sub: str,
        usr: UsrType,
) -> str:
    payload = {}
    expire = datetime.utcnow() + lifetime
    payload["type"] = token_type
    payload["exp"] = expire
    payload["iat"] = datetime.utcnow()
    payload["sub"] = str(sub)
    payload["usr"] = usr.value

    return jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=settings.ALGORITHM
    )
