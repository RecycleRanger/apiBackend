from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.crud.base import CRUDBase
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate


class CRUDStudent(CRUDBase[Student, StudentCreate, StudentUpdate]):

    def get_class(
            self,
            db: Session,
            class_id: int,
            skip: int = 0,
            limit: int = 100,
    ) -> List[Student]:
        return db.query(Student) \
                 .filter(Student.class_id == class_id) \
                 .offset(skip) \
                 .limit(limit) \
                 .all()

    def get_class_cens(
            self,
            db: Session,
            class_id: int,
            skip: int = 0,
            limit: int = 100,
    ) -> List[Student]:
        students = self.get_class(db=db, class_id=class_id, skip=skip, limit=limit)
        students = jsonable_encoder(students)
        for student in students:
            del student["hashed_password"]
            del student["numOfTrash"]

        return students

student = CRUDStudent(Student)