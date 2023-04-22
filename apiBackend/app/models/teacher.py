from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Teacher(Base):
    # __tablename__ = "teacher"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(256), nullable=False)
    hashed_password = Column(String, nullable=False)
    date_started = Column(DateTime, nullable=True)

    students = relationship("Student", back_populates="teacherSub")
