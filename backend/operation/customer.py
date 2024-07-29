import sqlalchemy
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.models import DBCustomer
from backend.operation.user import check_user
from backend.schema.customer import CustomerCreate, CustomerUpdate


class CustomerOperation:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_all_customers(self):
        query = sqlalchemy.select(DBCustomer)

        async with self.db_session as session:
            customers = await session.scalars(query)

        return [customer for customer in customers]

    async def get_customer_by_user_id(self, user_id: int):
        if not await check_user(user_id, self.db_session):
            raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found.")

        query = sqlalchemy.select(DBCustomer).filter(DBCustomer.user_id == user_id)

        async with self.db_session as session:
            customer = await session.scalar(query)
            if customer is None:
                raise HTTPException(status.HTTP_404_NOT_FOUND, "customer not found.")

            if not customer.active:
                raise HTTPException(status.HTTP_400_BAD_REQUEST, "bad request.")

        return customer

    async def create_customer(self, customer: CustomerCreate):
        if not await check_user(customer.user_id, self.db_session):
            raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found.")

        customer = DBCustomer(
            customer_type=customer.customer_type,
            active=customer.active,
            user_id=customer.user_id,
        )

        async with self.db_session as session:
            session.add(customer)
            await session.commit()
            await session.refresh(customer)

        return customer

    async def update_customer(self, id: int, data: dict):
        query = sqlalchemy.select(DBCustomer).where(DBCustomer.id == id)

        async with self.db_session as session:
            customer = await session.scalar(query)
            if customer is None:
                raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found.")
            for key, value in data.items():
                setattr(customer, key, value)
            await session.commit()
            await session.refresh(customer)

        return customer

    async def delete_customer(self, id: int):
        query = sqlalchemy.select(DBCustomer).where(DBCustomer.id == id)

        async with self.db_session as session:
            customer = await session.scalar(query)
            if customer is None:
                raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found.")
            await session.delete(customer)
            await session.commit()

        return customer
