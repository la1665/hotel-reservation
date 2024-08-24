import sqlalchemy
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from datetime import datetime

from exception_handeler import exceptions
from user.models import DBUser
from user.schema import UserBase, UserCreate, UserUpdate
from authentication import auth


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

        async with self.db_session as session:
            result = await session.execute(select(DBUser))
            users = result.scalars().all()

        return users

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
            data["updated_at"] = datetime.utcnow()
            for key, value in data.items():
                setattr(user, key, value)
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
