from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.teacher import Teacher
from app.schemas.teacher import TeacherCreate, TeacherUpdate
from app.core.security import get_password_hash


class CRUDTeacher(CRUDBase[Teacher, TeacherCreate, TeacherUpdate]):
    def create(
            self,
            db: Session,
            *,
            obj_in: TeacherCreate
    ) -> Teacher:
        create_data = obj_in.dict()
        create_data.pop("password")
        db_obj = Teacher(**create_data)
        db_obj.hashed_password = get_password_hash(obj_in.password)
        db.add(db_obj)
        db.commit()

        return db_obj

teacher = CRUDTeacher(Teacher)
