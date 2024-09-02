from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from exception_handeler import exceptions
from authentication.auth import get_user
from authentication.authorization import (
    get_current_user,
    get_current_active_user,
    is_admin_user,
)
from db.engine import get_db
from user.operation import UserOperation
from user.schema import UserInDB, UserCreate, UserUpdate, UserOut

router = APIRouter(tags=["user"])


@router.post("/users", response_model=UserInDB)
async def api_create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # db_user = await get_user(db=db, username=user.username)
    # if db_user:
    #     raise exceptions.NotAllowedException("User error", "Username already exists.")
    return await UserOperation(db).create_user(user)


@router.get("/users", response_model=list[UserOut])
async def api_read_all_user(
    db: AsyncSession = Depends(get_db),
    current_user: UserInDB = Depends(is_admin_user),
):
    users = await UserOperation(db).get_all_users()
    return users


@router.get("/users/me", response_model=UserOut)
async def api_users_me(
    db: AsyncSession = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user),
):
    user_id = current_user.id
    return await UserOperation(db).get_user(user_id)


@router.get("/users/{user_id}", response_model=UserOut)
async def api_read_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    if user_id != current_user.id and current_user.user_type.value != "admin":
        raise exceptions.NotAllowedException("Authorization Error", "Not Allowed!")
    user = await UserOperation(db).get_user(user_id)
    return user


@router.put("/users/{user_id}", response_model=UserInDB)
async def api_update_user(
    user_id: int,
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    # if user_id != current_user.id:
    #     raise exceptions.NotAllowedException("Authorization Error", "Not Allowed!")
    update_data = data.dict(exclude_unset=True)
    user = await UserOperation(db).update_user(user_id, update_data)
    return user


@router.delete("/users/{user_id}", response_model=UserInDB)
async def api_delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserInDB = Depends(get_current_user),
):
    if user_id != current_user.id and current_user.user_type.value != "admin":
        raise exceptions.NotAllowedException("Authorization Error", "Not Allowed!")
    user = await UserOperation(db).delete_user(user_id)
    return user
