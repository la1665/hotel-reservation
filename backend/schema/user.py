from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from backend.db.models import UserType


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


class UserInDB(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
