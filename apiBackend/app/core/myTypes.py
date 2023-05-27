from typing import Generic, TypeVar, Union
from enum import Enum
from dataclasses import dataclass
from pydantic import BaseModel

from app.models import Teacher
from app.models import Student


class UsrType(Enum):
    teacher = 1
    student = 2

@dataclass
class Payload:
    type: str
    exp: int
    iat: int
    sub: str
    usr: UsrType

User = TypeVar("User", Teacher, Student)

@dataclass
class CurrentUsr(Generic[User]):
    user: User
    type: UsrType
