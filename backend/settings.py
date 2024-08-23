# import os
# from dotenv import load_dotenv
from typing import Union, Optional, Any
from pydantic_settings import BaseSettings

# load_dotenv()
# DATABASE_URL = os.getenv("DATABASE_URL")
# SECRET_KEY: Any = os.getenv("SECRET_KEY")
# ACCESS_TOKEN_EXPIRE_MINUTES: Any = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
# ALGORITHM = "HS256"


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"


settings = Settings()
