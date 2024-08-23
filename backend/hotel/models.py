from sqlalchemy.sql import Nullable
from sqlalchemy.sql.sqltypes import Float, Integer, String, Boolean, Text, DateTime
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, func, Enum as sqlalchemyEnum
from enum import Enum

from db.engine import Base


class HotelType(Enum):
    FIVESTAR = "five-star"
    FOURSTAR = "four-star"
    MOTEL = "motel"
    ECONOMIC = "economic"


class IranCities(Enum):
    ABADAN = "abadan"
    ARAK = "arak"
    AHVAZ = "ahvaz"
    ARDABIL = "ardabil"
    BABOL = "babol"
    BANDARE_ABBAS = "bandar-e abbas"
    ESFAHAN = "esfahan"
    GORGAN = "gorgan"
    HAMEDAN = "hamedan"
    ILAM = "ilam"
    KERMMAN = "kerman"
    KERMANSHAH = "kermanshah"
    MASHHAD = "mashhad"
    RASHT = "rasht"
    SARI = "sari"
    SEMNAN = "semnan"
    TABRIZ = "tabriz"
    TEHRAN = "tehran"
    YAZD = "yazd"


class RoomType(Enum):
    NORMAL = "normal"
    VIP = "vip"
    LUXURY = "luxury"


class DBHotel(Base):
    __tablename__ = "hotel"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(250), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, nullable=False, default=func.now())
    hotel_type = Column(sqlalchemyEnum(HotelType), default=HotelType.ECONOMIC, nullable=False)
    city = Column(sqlalchemyEnum(IranCities), default=IranCities.TEHRAN, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    rating = Column(Float, default=0.0)
    rooms = relationship("DBRoom", back_populates="hotel", lazy="joined")


class DBRoom(Base):
    __tablename__ = "room"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    description = Column(Text)
    beds = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    room_type = Column(sqlalchemyEnum(RoomType), default=RoomType.NORMAL, nullable=False)
    price = Column(Integer, nullable=False)
    hotel_id = Column(Integer, ForeignKey("hotel.id"))
    hotel = relationship("DBHotel", back_populates="rooms")
