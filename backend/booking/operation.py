from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload, selectinload
from datetime import datetime

from hotel.models import DBRoom
from hotel.schema import RoomInDB
from booking.models import DBBooking
from booking.schema import BookingCreate
from exception_handeler import exceptions


class BookingOperation:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def create_booking(self, booking: BookingCreate, user_id: int, room_id: int):
        async with self.db_session as session:
            db_room = await session.execute(select(DBRoom).filter(DBRoom.id == room_id))
            db_room = db_room.scalars().first()
            if db_room is None:
                raise exceptions.NotFoundException("Room")
            # Check if room is already booked for the given dates
            result = await session.execute(
                select(DBBooking)
                .filter(DBBooking.room_id == room_id).filter(DBBooking.start_date < booking.end_date, DBBooking.end_date > booking.start_date))
            existing_booking = result.scalars().first()

            # existing_booking = result.scalars().first()
            if existing_booking:
                raise exceptions.BadRequestExceptions("Room is already booked for the selected dates.")

            new_booking = DBBooking(
                user_id=user_id,
                room_id=room_id,
                start_date=booking.start_date,
                end_date=booking.end_date
            )
            session.add(new_booking)
            await session.commit()
            await session.refresh(new_booking)

            return new_booking

    async def get_booking(self, booking_id: int):
        async with self.db_session as session:
            booking = await session.execute(select(DBBooking).where(DBBooking.id == booking_id).options(joinedload(DBBooking.room), joinedload(DBBooking.user)))
            if booking is None:
                raise exceptions.NotFoundException("Booking")
            return booking.unique().scalars().first()

    async def get_all_booking_by_room(self, room_id: int):
        async with self.db_session as session:
            # db_room = await session.execute(select(DBRoom).filter(DBRoom.id == room_id))
            # db_room = db_room.scalars().first()
            # if db_room is None:
            #     raise exceptions.NotFoundException("Room")
            result = await session.execute(select(DBBooking).filter(DBBooking.room_id == room_id).options(joinedload(DBBooking.room), joinedload(DBBooking.user)))
            bookings = result.unique().scalars().all()
            # if bookings is None:
            #     raise exceptions.NotFoundException("Booking")
            return bookings

    async def update_booking(self, booking_id: int, data: dict):
        async with self.db_session as session:

            result = await session.execute(select(DBBooking).filter(DBBooking.id == booking_id))
            booking = result.scalars().first()

            if not booking:
                raise Exception("Booking not found.")

            data["updated_at"] = datetime.utcnow()
            for key, value in data.items():
                setattr(booking, key, value)
            await session.commit()
            await session.refresh(booking)

            return booking

    async def delete_booking(self, booking_id: int):
        async with self.db_session as session:
            result = await session.execute(select(DBBooking).filter(DBBooking.id == booking_id))
            booking = result.scalars().first()

            if booking is None:
                raise exceptions.NotFoundException("Booking")

            await session.delete(booking)
            await session.commit()

            return booking
