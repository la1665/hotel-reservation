import os
from dotenv import load_dotenv
from typing import Union, Optional, Any

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY: Any = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES: Any = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
ALGORITHM = "HS256"
