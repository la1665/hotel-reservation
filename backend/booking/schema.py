from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional, List

from booking.models import DBBooking
from hotel.schema import RoomInDB
# from user.schema import UserInDB


class BookingBase(BaseModel):
    start_date: date
    end_date: date

class BookingCreate(BookingBase):
    # room_id: int = Field(exclude=True)
    pass

class BookingUpdate(BookingBase):
    pass

class BookingInDB(BookingBase):
    id: int
    user_id: int
    room_id: int
    created_at: datetime
    updated_at: datetime
    is_paid: bool = Field(default=False)
    total_price: float

    class Config:
        orm_mode = True

# class BookingOut(BookingInDB):
#     user: Optional[UserInDB]  # Customize as needed
#     room: Optional[RoomInDB]  # Customize as needed
