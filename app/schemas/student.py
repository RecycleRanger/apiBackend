from typing import Optional

from pydantic import BaseModel

from app.schemas.waste import Waste


class StudentBase(BaseModel):
    student_name: Optional[str] = None
    score: int
    class_id: int

class StudentCreate(StudentBase):
    password: str

class StudentUpdate(StudentBase):
    ...

class StudentInDBBase(StudentBase):
    id: int
    waste_tracking: list[Waste] = []

    class Config:
        orm_mode = True

class StudentInDB(StudentInDBBase):
    hashed_password: str

class Student(StudentInDBBase):
    ...
