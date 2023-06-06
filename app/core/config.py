import pathlib
from os import path

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, validator
from typing import List, Optional, Union


ROOT = pathlib.Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    PROJECT_NAME: str = "RecycleRanger"
    API_V1_STR: str = "/api/v1"
    JWT_SECRET: str = ""
    ALGORITHM: str = "HS256"

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # Change the origins when in production
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    SQLALCHEMY_DB_URI: str = ""

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(
            cls,
            v: Union[str, List[str]]
    ) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    SUPERUSER: str = "admin"

    class Config:
        case_sensitive = True
        env_file = path.join(ROOT, ".env")

settings = Settings()
