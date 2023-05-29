from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.db.base_class import Base
from app.core.myError import Result, Ok, Err


class NoUserFoundInDB(Exception):
    """Raised when query from database finds no match"""

    def __init__(self, msg="No User was found on the database."):
        self.message = msg
        super().__init__(self.message)

    def httpError(self):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No User was found on the database."
        )

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (shcema) class
        """

        self.model = model

    def get(self, db: Session, id: Any) -> Result[ModelType, NoUserFoundInDB]:
        search = db.query(self.model) \
                   .filter(self.model.id == id) \
                   .first()
        if not search:
            return Err(NoUserFoundInDB("No user was found in the database"))
        return Ok(search)

    def get_multi(
            self,
            db: Session,
            *,
            skip: int = 0,
            limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model) \
                 .offset(skip) \
                 .limit(limit) \
                 .all()

    def create(
            self,
            db: Session,
            *,
            obj_in: CreateSchemaType
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def update(
            self,
            db:Session,
            *,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def remove(
            self,
            db: Session,
            *,
            id: int
    ) -> ModelType | None:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()

        return obj
