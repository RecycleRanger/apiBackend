from pydantic import BaseModel


class WasteBase(BaseModel):
    student_id: int
    trash_type: str
    trash_score: int

class WasteCreate(WasteBase):
    ...

class WasteUpdate(WasteBase):
    ...

class WasteInDBBase(WasteBase):
    id: int

    class Config:
        orm_mode = True

class WasteInDB(WasteInDBBase):
    ...

class Waste(WasteInDBBase):
    ...
