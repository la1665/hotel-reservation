from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError

from settings import settings
from exception_handeler import exceptions
from db.engine import get_db
from authentication.auth import oauth2_scheme, get_user
from schema.auth import TokenData
from schema.user import UserInDB


async def get_current_user(
    db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username = payload.get("sub")
        if username is None:
            raise exceptions.UnauthorizedException(
                "Authorization Error",
                "Could not validate credentials",
                {"WWW-Authenticate": "Bearer"},
            )
        token_data = TokenData(username=username)
    except JWTError:
        raise exceptions.UnauthorizedException(
            "Authorization Error",
            "Could not validate credentials",
            {"WWW-Authenticate": "Bearer"},
        )
    user = await get_user(db, username=token_data.username)
    if user is None:
        raise exceptions.UnauthorizedException(
            "Authorization Error",
            "Could not validate credentials",
            {"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if not current_user.is_active:
        raise exceptions.NotAllowedException(
            "Authorization Error", "User is not active!"
        )
    return current_user


async def is_admin_user(current_user: UserInDB = Depends(get_current_active_user)):
    if not current_user.user_type.value == "admin":
        raise exceptions.NotAllowedException(
            "Authorization Error", "Not an admin user!"
        )
    return current_user
