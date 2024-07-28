import os
from fastapi import FastAPI, status
from dotenv import load_dotenv

from db.engine import db_init

app = FastAPI()
# Load environment variables from .env file
load_dotenv()
# Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")


@app.on_event("startup")
async def startup():
    await db_init(DATABASE_URL)


@app.get("/")
async def root_path() -> dict:
    return {"massage": "hello world!", "status": status.HTTP_200_OK}
