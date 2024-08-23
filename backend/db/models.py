# from enum import Enum
# from sqlalchemy import Column, func, Enum as sqlalchemyEnum
# from sqlalchemy.sql.schema import ForeignKey
# from sqlalchemy.sql.sqltypes import Boolean, Float, Integer, String, DateTime
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base


# Base = declarative_base()


# class UserType(Enum):
#     USER = "user"
#     ADMIN = "admin"


# class HotelType(Enum):
#     FIVESTAR = "five-star"
#     FOURSTAR = "fourstar"
#     MOTEL = "motel"


# class DBUser(Base):
#     __tablename__ = "user"
#     id = Column(Integer, primary_key=True, autoincrement=True, index=True)
#     first_name = Column(String(250), nullable=False)
#     last_name = Column(String(250), nullable=False)
#     username = Column(String(250), nullable=False, unique=True)
#     hashed_password = Column(String, nullable=False)
#     email_address = Column(String(250), nullable=False, unique=True)
#     created_at = Column(DateTime, nullable=False, default=func.now())
#     updated_at = Column(
#         DateTime, nullable=False, default=func.now(), onupdate=func.now()
#     )
#     user_type = Column(sqlalchemyEnum(UserType), default=UserType.USER, nullable=False)
#     is_active = Column(Boolean, nullable=False, default=True)


# class DBCustomer(Base):
#     __tablename__ = "customer"
#     id = Column(Integer, primary_key=True, autoincrement=True, index=True)
#     user_id = Column(Integer, ForeignKey("user.id"), unique=True, nullable=False)
#     user = relationship("DBUser", back_populates="customer")
#     customer_type = Column(
#         sqlalchemyEnum(CustomerType), default=CustomerType.BASIC, nullable=False
#     )


# class DBHotel(Base):
#     __tablename__ = "hotel"
#     id = Column(Integer, primary_key=True, autoincrement=True, index=True)
#     name = Column(String(250), nullable=False)
#     address = Column(String(250), nullable=False, unique=True)
#     hotel_type = Column(
#         sqlalchemyEnum(HotelType), default=HotelType.MOTEL, nullable=False
#     )
#     active = Column(Boolean, default=True, nullable=False)
#     rating = Column(Float, default=1)
#     total_rooms = Column(Integer, default=0)
#     room = relationship("DBRoom", uselist=True, back_populates="hotel")


# class DBRoom(Base):
#     __tablename__ = "room"
#     id = Column(Integer, primary_key=True, autoincrement=True, index=True)
#     number = Column(String(250), nullable=False)
#     room_type = Column(String(250), nullable=False, unique=True)
#     price = Column(Integer, nullable=False)
#     hotel_id = Column(Integer, ForeignKey("hotel.id"))
#     hotel = relationship("DBHotel", back_populates="rooms")


# class DBReservation(Base):
#     __tablename__ = "booking"
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     from_date = Column(DateTime, nullable=False)
#     to_date = Column(DateTime, nullable=False)
#     price = Column(Integer, nullable=False)
#     user_id = Column(Integer, ForeignKey("user.id"))
#     room_id = Column(Integer, ForeignKey("room.id"))
