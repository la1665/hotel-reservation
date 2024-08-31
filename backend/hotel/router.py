from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.engine import get_db
from authentication.authorization import is_admin_user, get_current_active_user
from exception_handeler import exceptions
from hotel.operation import HotelOperation, RoomOperation, get_hotel, get_hotel_by_id
from hotel.schema import HotelInDB, HotelCreate, HotelBase, RoomCreate, RoomInDB
from user.schema import UserInDB
from utils.weather_api import get_weather_for_city

hotel_router = APIRouter(tags=["hotel"])


@hotel_router.post("/hotels", response_model=HotelInDB)
async def api_create_hotel(hotel: HotelCreate, db: AsyncSession=Depends(get_db), current_user: UserInDB=Depends(is_admin_user)):
    # db_hotel = await get_hotel(db, hotel.name)
    # if db_hotel:
    #     raise exceptions.NotAllowedException("Hotel creation error", "hotel  already exists.")
    return await HotelOperation(db).create_hotel(hotel)


@hotel_router.get("/hotels", response_model=list[HotelInDB])
async def api_read_all_hotel(db: AsyncSession=Depends(get_db), current_user: UserInDB=Depends(get_current_active_user)):
    hotels = await HotelOperation(db).get_all_hotels()
    return hotels


@hotel_router.get("/hotels/{hotel_id}", response_model=HotelInDB)
async def api_read_hotel(hotel_id: int, db: AsyncSession=Depends(get_db), current_user: UserInDB=Depends(get_current_active_user)):
    hotel = await HotelOperation(db).get_hotel(hotel_id)
    return hotel


@hotel_router.get("/hotels/{hotel_id}/weather")
async def api_hotel_weather(hotel_id: int, db: AsyncSession = Depends(get_db)):
    hotel = await HotelOperation(db).get_hotel(hotel_id)
    city = hotel.city.value
    weather_data = get_weather_for_city(city)
    if weather_data is None:
        raise exceptions.NotFoundException("Weather")

    return {"city": hotel.city, "weather": weather_data}


room_router = APIRouter(tags=["room"])


@room_router.post("/hotels/{hotel_id}/rooms", response_model=RoomInDB)
async def api_create_room(hotel_id: int, room: RoomCreate, db: AsyncSession=Depends(get_db), current_user:UserInDB=Depends(is_admin_user)):
    if await HotelOperation(db).get_hotel(hotel_id) is None:
        raise exceptions.NotFoundException("Hotel")
    # if get_hotel_by_id(db, hotel_id) is None:
    #     raise exceptions.NotFoundException("Hotel")
    return await RoomOperation(db).create_room(room, hotel_id)


@room_router.get("/rooms", response_model=list[RoomInDB])
async def api_read_all_rooms(hotel_id: int | None = None, db: AsyncSession=Depends(get_db), current_user:UserInDB=Depends(is_admin_user)):
    rooms = await RoomOperation(db).get_all_rooms(hotel_id)
    return rooms


@room_router.get("/hotels/{hotel_id}/rooms", response_model=list[RoomInDB])
async def api_read_all_rooms_by_hotel(hotel_id:int, db: AsyncSession=Depends(get_db), current_user:UserInDB=Depends(get_current_active_user)):
    rooms = await RoomOperation(db).get_all_rooms(hotel_id)
    return rooms
