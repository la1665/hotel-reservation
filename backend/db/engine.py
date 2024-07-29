import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncEngine
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()
# Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")


engine: AsyncEngine
engine = create_async_engine(DATABASE_URL)
DBSession = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)
Base = declarative_base()


async def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        await db.close()
