from sqlalchemy import Column, func, Enum as sqlalchemyEnum
from sqlalchemy.sql.sqltypes import Boolean, Float, Integer, String, DateTime
from sqlalchemy.orm import relationship
from enum import Enum

from db.engine import Base


class UserType(Enum):
    USER = "user"
    ADMIN = "admin"


class OfferType(Enum):
    ZERO = 0.0
    TENPERCENT = 0.1
    TWOPERCENT = 0.2
    THREEPERCENT = 0.3
    FOURPERCENT = 0.4
    FIVEPERCENT = 0.5
    VIPOFFER = 0.75


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
    offer_type = Column(sqlalchemyEnum(OfferType), default=OfferType.ZERO, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    bookings = relationship("DBBooking", back_populates="user", lazy="joined", cascade="all, delete-orphan")
