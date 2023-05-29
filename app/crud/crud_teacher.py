from typing import Any, Dict, Optional, Union, List
from datetime import datetime

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.teacher import Teacher
from app.schemas.teacher import TeacherCreate, TeacherUpdate
from app.core.security import get_password_hash
from app.core.myError import Result, Ok, Err


class CRUDTeacher(CRUDBase[Teacher, TeacherCreate, TeacherUpdate]):
    def create(
            self,
            db: Session,
            *,
            obj_in: TeacherCreate
    ) -> Teacher:
        create_data = obj_in.dict()
        create_data.pop("password")
        db_obj: Teacher = Teacher(**create_data) # type: ignore
        db_obj.hashed_password = get_password_hash(obj_in.password) # type: ignore
        db.add(db_obj)
        db.commit()

        return db_obj

    def update_datetime(
            self,
            *,
            db: Session,
            teacher_id: int,
    ) -> bool:
        match self.get(db, teacher_id):
            case Ok(v): hasStarted: Teacher = v
            case Err(e): raise e
        query = 0
        if not bool(hasStarted.date_started):
            query = db.query(Teacher) \
                    .filter(Teacher.id == teacher_id) \
                    .update({Teacher.date_started: datetime.now()}, synchronize_session=False)
            db.commit()
        return not not query

teacher = CRUDTeacher(Teacher)
