from enum import Enum
from dataclasses import dataclass


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
