from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class Waste(Base):
    # __tablename__ = "waste"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student.id"), nullable=False)
    createdAt = Column(DateTime, server_default=func.now(), nullable=False)
    trash_type = Column(String, nullable=False)
    trash_score = Column(Integer, nullable=False)

    student = relationship("Student", back_populates="waste_tracking")
