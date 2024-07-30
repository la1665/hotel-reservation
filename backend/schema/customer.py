from pydantic import BaseModel, Field
from sqlalchemy.sql.type_api import _BaseTypeMemoDict

from backend.db.models import CustomerType


class CustomerBase(BaseModel):
    customer_type: CustomerType = Field(default=CustomerType.BASIC)


class CustomerCreate(CustomerBase):
    user_id: int = Field(exclude=True)


class CustomerUpdate(CustomerBase):
    pass


class CustomerInDB(CustomerBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class CustomerOutput(CustomerInDB):
    user: str
