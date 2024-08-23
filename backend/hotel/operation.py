import sqlalchemy
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload
from datetime import datetime

from exception_handeler import exceptions
from hotel.models import DBHotel, DBRoom
from hotel.schema import HotelBase, HotelCreate, HotelInDB, RoomBase, RoomCreate, RoomInDB
from authentication import auth


class HotelOperation:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def create_hotel(self, hotel: HotelCreate):
        hotel = DBHotel(
            name=hotel.name,
            description=hotel.description,
            hotel_type=hotel.hotel_type,
            city=hotel.city,
            rating=hotel.rating
        )
        async with self.db_session as session:
            session.add(hotel)
            await session.commit()
            await session.refresh(hotel)
        return hotel

    async def get_hotel(self, hotel_id: int):
        query = sqlalchemy.select(DBHotel).where(DBHotel.id == hotel_id)
        async with self.db_session as session:
            hotel = await session.scalar(query)
            if hotel is None:
                raise exceptions.NotFoundException("Hotel")

            return hotel

    async def get_all_hotels(self):
        query = sqlalchemy.select(DBHotel)
        async with self.db_session as session:
            result = await session.execute(select(DBHotel).options(selectinload(DBHotel.rooms)))  # Eager load rooms)
            hotels = result.scalars().all()  # Fetch all hotels
            # hotels = await session.execute(select(DBHotel).unique())
            # hotels = await session.scalars(query)
        # return [hotel for hotel in hotels]
        return hotels
