from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

from booking.schema import BookingInDB
from user.models import UserType, OfferType


class UserBase(BaseModel):
    username: str
    email_address: str
    first_name: str
    last_name: str
    is_active: bool = Field(default=True)
    user_type: UserType = Field(default=UserType.USER)


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email_address: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    user_type: UserType = Field(default=UserType.USER)

    class Config:
        orm_mode = True


class UserInDB(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    offer_type: OfferType = Field(default=OfferType.ZERO)
    bookings: List[BookingInDB] = []

    class Config:
        orm_mode = True
