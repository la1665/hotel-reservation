import sqlalchemy
from sqlalchemy.future import select
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.exception_handeler import exceptions
from backend.db.models import DBCustomer, DBUser
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
        query = sqlalchemy.select(DBCustomer).filter(DBCustomer.user_id == user_id)

        async with self.db_session as session:
            customer = await session.scalar(query)
            if customer is None:
                raise exceptions.NotFoundException("Customer")

        return customer

    async def create_customer(self, customer: CustomerCreate):
        async with self.db_session as session:
            result = await session.execute(
                select(DBCustomer).filter(DBCustomer.user_id == customer.user_id)
            )
            if result.scalars().first():
                raise exceptions.BadRequestExceptions("Customer already exists!")

            customer = DBCustomer(
                customer_type=customer.customer_type,
                user_id=customer.user_id,
            )
            session.add(customer)
            await session.commit()
            await session.refresh(customer)

        return customer

    async def update_customer(self, id: int, data: dict):
        query = sqlalchemy.select(DBCustomer).where(DBCustomer.id == id)
        async with self.db_session as session:
            customer = await session.scalar(query)
            if customer is None:
                raise exceptions.NotFoundException("Customer")
            if customer.user_id != data.get("user_id"):
                raise exceptions.NotAllowedException(
                    "Authorization Error", "Not Allowed!"
                )
            for key, value in data.items():
                setattr(customer, key, value)
            await session.commit()
            await session.refresh(customer)

        return customer

    async def delete_customer(self, id: int, data: dict = {}):
        query = sqlalchemy.select(DBCustomer).where(DBCustomer.id == id)
        async with self.db_session as session:
            customer = await session.scalar(query)
            if customer is None:
                raise exceptions.NotFoundException("Customer")
            if customer.user_id != data.get("user_id"):
                raise exceptions.NotAllowedException(
                    "Authorization Error", "Not Allowed!"
                )
            await session.delete(customer)
            await session.commit()

        return customer

    async def force_delete_customer(self, id: int, data: dict = {}):
        query = sqlalchemy.select(DBCustomer).where(DBCustomer.id == id)
        async with self.db_session as session:
            customer = await session.scalar(query)
            if customer is None:
                raise exceptions.NotFoundException("Customer")
            await session.delete(customer)
            await session.commit()

        return customer
