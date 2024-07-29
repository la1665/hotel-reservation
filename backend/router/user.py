from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.engine import get_db
from backend.operation.user import UserOperation
from backend.schema.user import UserBase, UserInDB, UserCreate, UserUpdate


router = APIRouter()


@router.post("/users", response_model=UserInDB)
async def api_create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await UserOperation(db).create_user(user)


@router.get("/users")
async def api_read_all_user(db: AsyncSession = Depends(get_db)):
    users = await UserOperation(db).get_all_users()
    return users


@router.get("/users/{user_id}")
async def api_read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await UserOperation(db).get_user(user_id)
    return user


@router.put("/users/{user_id}", response_model=UserInDB)
async def api_update_user(
    user_id: int, data: UserUpdate, db: AsyncSession = Depends(get_db)
):
    user = await UserOperation(db).update_user(user_id, data.dict())
    return user


@router.delete("/users/{user_id}")
async def api_delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await UserOperation(db).delete_user(user_id)
    return user
