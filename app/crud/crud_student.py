from threading import excepthook
from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from fastapi.encoders import jsonable_encoder

from app.crud.base import CRUDBase, NoUserFoundInDB, InvalidDataQuery
from app.models.student import Student
from app.models.teacher import Teacher
from app.schemas.student import StudentCreate, StudentUpdate
from app.core.security import get_password_hash
from app.core.myError import Result, Ok, Err
from app.crud.crud_teacher import teacher


class CRUDStudent(CRUDBase[Student, StudentCreate, StudentUpdate]):

    def create(
            self,
            db: Session,
            *,
            obj_in: StudentCreate
    ) -> Student:
        match teacher.get(db=db, id=obj_in.class_id):
            case Ok(v):
                create_data = obj_in.dict()
                create_data.pop("password")
                db_obj = Student(**create_data) # type: ignore
                db_obj.hashed_password = get_password_hash(obj_in.password) # type: ignore
                db.add(db_obj)
                db.commit()

                return db_obj
            case Err(e):
                raise e.httpError() from e

    def get_by_username(
            self,
            db: Session,
            username: str,
    ) -> Result[Student, NoUserFoundInDB | InvalidDataQuery]:
        try:
            search = db.query(Student) \
                    .filter(Student.student_name == username) \
                    .first()
        except OperationalError:
            return Err(InvalidDataQuery())
        if not search:
            return Err(NoUserFoundInDB("No user found in the database"))
        return Ok(search)

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
    ) -> Any:
        students = self.get_class(db=db, class_id=class_id, skip=skip, limit=limit)
        students = jsonable_encoder(students)

        for student in students:
            del student["hashed_password"]
            del student["numOfTrash"]

        return students

    def update_name(
            self,
            *,
            db: Session,
            student_id: int,
            newName: str,
    ) -> bool:

        try:
            query = db.query(Student) \
                      .filter(Student.id == student_id) \
                      .update({Student.student_name: newName}, synchronize_session=False)
            db.commit()
            return bool(query)
        except:
            raise NoUserFoundInDB

    def update_password(
            self,
            *,
            db: Session,
            student_id: int,
            newPassword: str,
    ) -> bool:

        try:
            query = db.query(Student) \
                      .filter(Student.id == student_id) \
                      .update({Student.hashed_password: get_password_hash(newPassword)}, synchronize_session=False)
            db.commit()
            return bool(query)
        except:
            raise NoUserFoundInDB

    def update_score(
            self,
            *,
            db: Session,
            student_id: int,
            newScore: int,
    ) -> bool:

        try:
            query = db.query(Student) \
                      .filter(Student.id == student_id) \
                      .update({Student.score: newScore}, synchronize_session=False)
            db.commit()
            return bool(query)
        except:
            raise NoUserFoundInDB

    def update_numOfTrash(
            self,
            *,
            db: Session,
            student_id: int,
    ) -> bool:

        try:
            match self.get(db=db, id=student_id):
                case Ok(v):
                    if v.numOfTrash == None: # type: ignore
                        numOfTrash = 1
                    else:
                        numOfTrash = v.numOfTrash + 1
                case Err(e):
                    raise e.httpError() from e
            query = db.query(Student) \
                      .filter(Student.id == student_id) \
                      .update({Student.numOfTrash: numOfTrash}, synchronize_session=False)
            db.commit()
            return bool(query)
        except:
            raise NoUserFoundInDB

student = CRUDStudent(Student)
