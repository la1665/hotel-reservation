from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.authentication.auth import get_user
from backend.authentication.authorization import get_current_user, get_current_active_user, is_admin_user
from backend.db.engine import get_db
from backend.operation.user import UserOperation
from backend.schema.user import UserInDB, UserCreate, UserUpdate

router = APIRouter()


@router.post("/users", response_model=UserInDB)
async def api_create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await get_user(db=db, username=user.username)
    if db_user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Username already exists.")
    return await UserOperation(db).create_user(user)


@router.get("/users")
async def api_read_all_user(
    db: AsyncSession = Depends(get_db),
    current_user: UserInDB = Depends(is_admin_user),
):
    users = await UserOperation(db).get_all_users()
    return users

@router.get("/users/me", response_model=UserInDB)
async def api_users_me(db: AsyncSession=Depends(get_db), current_user: UserInDB = Depends(get_current_user)):
    user_id = current_user.id
    return await UserOperation(db).get_user(user_id)

@router.get("/users/{user_id}")
async def api_read_user(user_id: int, db: AsyncSession = Depends(get_db), current_user: UserInDB=Depends(get_current_active_user)):
    if user_id != current_user.id and current_user.user_type.value != "admin":
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "not allowed!")
    user = await UserOperation(db).get_user(user_id)
    return user


@router.put("/users/{user_id}", response_model=UserInDB)
async def api_update_user(
    user_id: int, data: UserUpdate, db: AsyncSession = Depends(get_db), current_user: UserInDB=Depends(get_current_active_user)
):
    if user_id != current_user.id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "not allowed!")
    user = await UserOperation(db).update_user(user_id, data.dict())
    return user


@router.delete("/users/{user_id}")
async def api_delete_user(user_id: int, db: AsyncSession = Depends(get_db), current_user: UserInDB = Depends(get_current_active_user)):
    if user_id != current_user.id and current_user.user_type.value != "admin":
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "not allowed!")
    user = await UserOperation(db).delete_user(user_id)
    return user
