from typing import Any
from sqlalchemy.engine import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine: Engine
DBSession = sessionmaker()
Base = declarative_base()


async def db_init(file: str | None):
    engine = create_engine(file)
    Base.metadata.bind = engine
    DBSession.configure(bind=engine)
