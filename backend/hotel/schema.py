from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

from hotel.models import HotelType, IranCities, RoomType


class RoomBase(BaseModel):
    description: str
    beds: int = Field(default=0)
    room_type: RoomType = Field(default=RoomType.NORMAL)
    price: int


class RoomCreate(RoomBase):
    # hotel_id: int = Field(exclude=True)
    pass


class RoomInDB(RoomBase):
    id: int
    hotel_id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool = Field(default=True)

    class Config:
        orm_mode = True


class HotelBase(BaseModel):
    name: str
    description: str
    hotel_type: HotelType = Field(default=HotelType.ECONOMIC)
    city: IranCities = Field(default=IranCities.TEHRAN)
    rating: float = Field(default=0.0)


class HotelCreate(HotelBase):
    pass


class HotelInDB(HotelBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool = Field(default=True)
    rooms: List[RoomInDB] = []

    class Config:
        orm_mode = True
