from sqlalchemy.orm import Session

from app.crud.base import CRUDBase, NoUserFoundInDB
from app.models import Waste
from app.schemas.waste import WasteCreate, WasteUpdate
from app.core.myError import Result, Ok, Err


class CRUDWaste(CRUDBase[Waste, WasteCreate, WasteUpdate]):

    def get_all(
            self,
            db: Session,
            student_id: int,
            *,
            skip: int = 0,
            limit: int = 100,
    ) -> Result[list[Waste], NoUserFoundInDB]:
        search = db.query(Waste) \
                   .filter(Waste.student_id == student_id) \
                   .offset(skip) \
                   .limit(limit) \
                   .all()
        if not search:
            return Err(NoUserFoundInDB("No item found in the database"))
        return Ok(search)

waste = CRUDWaste(Waste)
