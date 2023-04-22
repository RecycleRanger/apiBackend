from pydantic import BaseModel

from app.schemas.waste import Waste


class StudentBase(BaseModel):
    student_name: str
    score: int
    class_id: int

class StudentCreate(StudentBase):
    hashed_password: str

class StudentUpdate(StudentBase):
    ...

class Student(StudentBase):
    id: int
    waste_tracking: list[Waste] = []

    class Config:
        orm_mode = True
