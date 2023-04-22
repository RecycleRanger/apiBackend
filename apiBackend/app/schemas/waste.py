from pydantic import BaseModel

from app.schemas.waste import Waste


class WasteBase(BaseModel):
    student_id: int
    trash_type: str
    trash_score: int

class WasteCreate(WasteBase):
    ...

class WasteUpdate(WasteBase):
    ...

class Waste(WasteBase):
    id: int

    class Config:
        orm_mode = True
