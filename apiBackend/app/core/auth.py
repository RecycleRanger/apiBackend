from typing import Optional, MutableMapping, List, Union
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session
from jose import jwt

from app.models.teacher import Teacher
from app.models.student import Student
from app import schemas
from app.core.config import settings
from app.core.security import verify_password


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
        username: str,
        password: str,
        db: Session,
        usrType: str,
) -> Teacher | Student | None:

    # type: ignore
    if usrType == "teacher":
        user = db.query(Teacher) \
                    .filter(Teacher.username == username) \
                    .first()
    else:
        user = db.query(Student) \
                 .filter(Student.student_name == username) \
                 .first()

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(*, sub: str, usr: str) -> str:
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
        usr: str,
) -> str:
    payload = {}
    expire = datetime.utcnow() + lifetime
    payload["type"] = token_type
    payload["exp"] = expire
    payload["iat"] = datetime.utcnow()
    payload["sub"] = str(sub)
    payload["usr"] = str(usr)

    return jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=settings.ALGORITHM
    )
