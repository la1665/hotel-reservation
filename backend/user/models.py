from enum import Enum
from sqlalchemy import Column, func, Enum as sqlalchemyEnum
from sqlalchemy.sql.sqltypes import Boolean, Float, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

from db.engine import Base


class UserType(Enum):
    USER = "user"
    ADMIN = "admin"


class DBUser(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=False)
    username = Column(String(250), nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    email_address = Column(String(250), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )
    user_type = Column(sqlalchemyEnum(UserType), default=UserType.USER, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
