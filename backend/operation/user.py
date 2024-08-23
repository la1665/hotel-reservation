import sqlalchemy
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from datetime import datetime

from exception_handeler import exceptions
from db.models import DBUser
from schema.user import UserBase, UserCreate, UserUpdate
from authentication import auth


async def check_user(user_id: int, db_session: AsyncSession):
    result = await db_session.scalar(
        sqlalchemy.select(DBUser).filter(DBUser.id == user_id)
    )
    return result is not None


class UserOperation:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def get_user(self, user_id: int):
        query = sqlalchemy.select(DBUser).where(DBUser.id == user_id)

        async with self.db_session as session:
            user = await session.scalar(query)
            if user is None:
                raise exceptions.NotFoundException("User")

            return user

    async def get_all_users(self):
        query = sqlalchemy.select(DBUser)

        async with self.db_session as session:
            users = await session.scalars(query)

            return [user for user in users]

    async def create_user(self, user: UserCreate):
        hashed_password = auth.get_password_hash(user.password)
        user = DBUser(
            first_name=user.first_name,
            last_name=user.last_name,
            email_address=user.email_address,
            username=user.username,
            is_active=user.is_active,
            user_type=user.user_type,
            hashed_password=hashed_password,
        )

        async with self.db_session as session:
            session.add(user)
            await session.commit()
            await session.refresh(user)

        return user

    async def update_user(self, user_id: int, data: dict):
        query = sqlalchemy.select(DBUser).where(DBUser.id == user_id)

        async with self.db_session as session:
            user = await session.scalar(query)
            if user is None:
                raise exceptions.NotFoundException("User")
            for key, value in data.items():
                setattr(user, key, value)
            user.updated_at = (
                datetime.utcnow()
            )  # Update the timestamp for the last update
            await session.commit()
            await session.refresh(user)

            return user

    async def delete_user(self, user_id: int):
        query = sqlalchemy.select(DBUser).where(DBUser.id == user_id)

        async with self.db_session as session:
            user = await session.scalar(query)
            if user is None:
                raise exceptions.NotFoundException("User")
            await session.delete(user)
            await session.commit()

            return user
