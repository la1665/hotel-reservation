from enum import Enum
from typing import Any
from sqlalchemy import Column, func, Enum as sqlalchemyEnum
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, Float, Integer, String, DateTime
from sqlalchemy.orm import relationship

from backend.db.engine import Base


def to_dict(obj: Base) -> dict[str, Any]:
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}


class UserType(Enum):
    USER = "user"
    ADMIN = "admin"


class CustomerType(Enum):
    BASIC = "basic"
    PRO = "pro"
    VIP = "vip"


class HotelType(Enum):
    FIVESTAR = "five-star"
    FOURSTAR = "fourstar"
    MOTEL = "motel"


class DBUser(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=False)
    username = Column(String(250), nullable=False)
    email_address = Column(String(250), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )
    customer = relationship("DBCustomer", uselist=False, back_populates="user")


class DBCustomer(Base):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), unique=True, nullable=False)
    user = relationship("DBUser", back_populates="customer")
    customer_type = Column(
        sqlalchemyEnum(CustomerType), default=CustomerType.BASIC, nullable=False
    )
    active = Column(Boolean, default=True, nullable=False)


class DBHotel(Base):
    __tablename__ = "hotel"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(250), nullable=False)
    address = Column(String(250), nullable=False, unique=True)
    hotel_type = Column(
        sqlalchemyEnum(HotelType), default=HotelType.MOTEL, nullable=False
    )
    active = Column(Boolean, default=True, nullable=False)
    rating = Column(Float, default=1)
    rooms_total = Column(Integer, default=0)


class DBRoom(Base):
    __tablename__ = "room"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    number = Column(String(250), nullable=False)
    room_type = Column(String(250), nullable=False, unique=True)
    price = Column(Integer, nullable=False)
    hotel_id = Column(Integer, ForeignKey("hotel.id"))


class DBReservation(Base):
    __tablename__ = "booking"
    id = Column(Integer, primary_key=True, autoincrement=True)
    from_date = Column(DateTime, nullable=False)
    to_date = Column(DateTime, nullable=False)
    price = Column(Integer, nullable=False)
    customer_id = Column(Integer, ForeignKey("customer.id"))
    room_id = Column(Integer, ForeignKey("room.id"))
