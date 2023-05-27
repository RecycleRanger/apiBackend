from datetime import date, datetime, timedelta

from pydantic import BaseModel

from typing import Sequence
from app.schemas.student import Student


class TeacherBase(BaseModel):
    username: str

class TeacherCreate(TeacherBase):
    password: str

class TeacherUpdate(TeacherBase):
    date_started: timedelta

class TeacherInDBBase(TeacherBase):
    id: int
    # students: list[Student] = []

    class Config:
        orm_mode = True

class TeacherInDB(TeacherInDBBase):
    hashed_password: str

class Teacher(TeacherInDBBase):
    ...
