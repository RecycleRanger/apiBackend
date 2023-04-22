from pydantic import BaseModel

from typing import Sequence
from app.schemas.student import Student


class TeacherBase(BaseModel):
    username: str

class TeacherCreate(TeacherBase):
    hashed_password: str

class TeacherUpdate(TeacherBase):
    ...

class Teacher(TeacherBase):
    id: int
    students: list[Student] = []

    class Config:
        orm_mode = True
