from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth import auth
from backend.db.engine import get_db
from backend.operation.user import UserOperation
from backend.schema.user import UserInDB, UserCreate, UserUpdate


router = APIRouter()


@router.post("/users", response_model=UserInDB)
async def api_create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await auth.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return await UserOperation(db).create_user(user)


@router.get("/users")
async def api_read_all_user(
    db: AsyncSession = Depends(get_db),
    current_user: UserInDB = Depends(auth.get_current_active_user_is_admin),
):
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


@router.get("/users/me/", response_model=UserInDB)
async def api_users_me(current_user: UserInDB = Depends(auth.get_current_active_user)):
    return current_user
