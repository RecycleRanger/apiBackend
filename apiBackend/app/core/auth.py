from typing import Optional, MutableMapping, List, Union
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session
from jose import jwt

from app.models.teacher import Teacher
from app import schemas
from app.core.config import settings
from app.core.security import verify_password


JWTPayloadMapping = MutableMapping[
    str,
    Union[datetime, bool, str, List[str], List[int]]
]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login/teacher")

def authenticate(
        *,
        username: str,
        password: str,
        db: Session,
) -> Optional[Teacher]:

    # type: ignore
    teacher = db.query(Teacher) \
                .filter(Teacher.username == username) \
                .first()

    if not teacher:
        return None
    if not verify_password(password, teacher.hashed_password):
        return None
    return teacher

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
