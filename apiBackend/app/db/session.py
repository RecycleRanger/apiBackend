from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings


engine = create_engine(
    settings.SQLALCHEMY_DB_URI,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
