from enum import Enum
from sqlalchemy import Column, func, Enum as sqlalchemyEnum
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, Float, Integer, String, Date

from db.engine import Base


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
    email_address = Column(String(250), nullable=False, unique=True)
    created_at = Column(Date, nullable=False, default=func.now())
    updated_at = Column(Date, nullable=False, default=func.now(), onupdate=func.now())


class DBCustomer(Base):
    __tablename__ = "customer"
    user_id = Column(Integer, ForeignKey("user.id"))
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
    from_date = Column(Date, nullable=False)
    to_date = Column(Date, nullable=False)
    price = Column(Integer, nullable=False)
    customer_id = Column(Integer, ForeignKey("customer.id"))
    room_id = Column(Integer, ForeignKey("room.id"))
