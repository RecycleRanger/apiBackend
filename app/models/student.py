from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .waste import Waste
    from .teacher import Teacher

class Student(Base):
    # __tablename__ = "student"

    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String(256), nullable=True)
    hashed_password = Column(String, nullable=False)
    score = Column(Integer, nullable=True)
    numOfTrash = Column(Integer, nullable=True)

    class_id = Column(Integer, ForeignKey("teacher.id"), nullable=True)

    teacherSub = relationship("Teacher", back_populates="students")

    waste_tracking = relationship("Waste", back_populates="student_owner")
