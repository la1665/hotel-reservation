from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError

from settings import SECRET_KEY, ALGORITHM
from backend.db.engine import get_db
from backend.authentication.auth import oauth2_scheme, get_user
from backend.schema.auth import TokenData
from backend.schema.user import UserInDB

async def get_current_user(
    db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user


async def is_admin_user(
    current_user: UserInDB = Depends(get_current_active_user),
):
    if not current_user.user_type.value == "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="access denied!"
        )
    return current_user
