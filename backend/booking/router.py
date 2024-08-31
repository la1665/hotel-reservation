from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from booking.schema import BookingCreate, BookingInDB, BookingUpdate
from booking.operation import BookingOperation
from db.engine import get_db
from authentication.authorization import get_current_active_user
from user.schema import UserInDB
from exception_handeler import exceptions
from hotel.operation import RoomOperation

booking_router = APIRouter(tags=["bookings"])


@booking_router.post("/rooms/{room_id}/bookings")
async def api_create_booking(
    room_id: int,
    booking: BookingCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    # room = await RoomOperation(db).get_room(room_id)
    # if room is None:
    #     raise exceptions.NotFoundException("Room")
    new_booking = await BookingOperation(db).create_booking(booking, current_user.id, room_id)
    # new_booking = await booking_op.create_booking(booking, user_id=current_user.id)
    return new_booking


@booking_router.get("/bookings/{booking_id}", response_model=BookingInDB)
async def api_get_booking(booking_id: int, db: AsyncSession = Depends(get_db), user_id: UserInDB=Depends(get_current_active_user)):
    booking_op = BookingOperation(db)
    booking = await booking_op.get_booking(booking_id)
    if not booking:
        raise exceptions.NotFoundException("Booking")
    if user_id.id != booking.user_id and user_id.user_type.value != "admin":
        raise exceptions.NotAllowedException("Authorization", "you dont have enough permissions.!")
    return booking

@booking_router.get("/rooms/{room_id}/bookings", response_model=list[BookingInDB])
async def api_get_all_bookings(room_id: int, db: AsyncSession=Depends(get_db), current_user: UserInDB=Depends(get_current_active_user)):
    return await BookingOperation(db).get_all_booking_by_room(room_id)

@booking_router.put("/bookings/{booking_id}", response_model=BookingInDB)
async def api_update_booking(
    booking_id: int,
    booking: BookingUpdate,
    db: AsyncSession = Depends(get_db),
    cuurent_user: UserInDB=Depends(get_current_active_user)
):
    db_booking = await BookingOperation(db).get_booking(booking_id)
    if db_booking is None:
        raise exceptions.NotFoundException("Booking")
    if cuurent_user.id != db_booking.user_id and cuurent_user.user_type.value != "admin":
        raise exceptions.NotAllowedException("Authorization","You are not allowed to do this action.")
    booking_data = booking.dict(exclude_unset=True)
    booking = await BookingOperation(db).update_booking(booking_id, booking_data)
    return booking

@booking_router.delete("/bookings/{booking_id}", response_model=BookingInDB)
async def api_delete_booking(booking_id: int, db: AsyncSession = Depends(get_db), current_user: UserInDB=Depends(get_current_active_user)):
    booking_op = BookingOperation(db)
    booking = await booking_op.get_booking(booking_id)
    if not booking:
        raise exceptions.NotFoundException("Booking")
    if current_user.id != booking.user_id and current_user.user_type.value != "admin":
        raise exceptions.NotAllowedException("Authorization", "you dont have enough permissions.!")
    deleted_booking = await booking_op.delete_booking(booking_id)
    return deleted_booking
