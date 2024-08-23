from types import GetSetDescriptorType
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from hotel.models import DBHotel
from exception_handeler import exceptions
from db.engine import get_db
from hotel.operation import HotelOperation
from hotel.schema import HotelInDB, HotelCreate, HotelBase

hotel_router = APIRouter(tags=["hotel"])


async def get_hotel(db: AsyncSession, hotel_name: str | None):
    result = await db.execute(select(DBHotel).filter(DBHotel.name == hotel_name))
    return result.scalars().first()


@hotel_router.post("/hotels", response_model=HotelInDB)
async def api_create_hotel(hotel: HotelCreate, db: AsyncSession=Depends(get_db)):
    db_hotel = await get_hotel(db, hotel.name)
    if db_hotel:
        raise exceptions.NotAllowedException("Hotel creation error", "hotel  already exists.")
    return await HotelOperation(db).create_hotel(hotel)


@hotel_router.get("/hotels")
async def api_read_all_hotel(db: AsyncSession=Depends(get_db)):
    hotels = await HotelOperation(db).get_all_hotels()
    return hotels


@hotel_router.get("/hotels/{hotel_id}")
async def api_read_hotel(hotel_id: int, db: AsyncSession=Depends(get_db)):
    hotel = await HotelOperation(db).get_hotel(hotel_id)
    return hotel
