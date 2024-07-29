from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.engine import get_db
from backend.operation.customer import CustomerOperation
from backend.schema.customer import (
    CustomerCreate,
    CustomerInDB,
    CustomerOutput,
    CustomerUpdate,
)

router = APIRouter()


@router.get(
    "/customers",
)
async def api_read_all_customer(db: AsyncSession = Depends(get_db)):
    customers = await CustomerOperation(db).get_all_customers()
    return customers


@router.get("/customers/{user_id}")
async def api_get_customer_by_user_id(user_id: int, db: AsyncSession = Depends(get_db)):
    customer = await CustomerOperation(db).get_customer_by_user_id(user_id)
    return customer


@router.post("/customers", response_model=CustomerInDB)
async def api_create_customer(
    customer: CustomerCreate, db: AsyncSession = Depends(get_db)
):
    return await CustomerOperation(db).create_customer(customer)


@router.put("/customers/{customer_id}")
async def api_update_customer(
    customer_id: int, customer: CustomerUpdate, db: AsyncSession = Depends(get_db)
):
    customer = await CustomerOperation(db).update_customer(customer_id, customer.dict())
    return customer


@router.delete("/customer/{customer_id}")
async def api_delete_customer(customer_id: int, db: AsyncSession = Depends(get_db)):
    customer = await CustomerOperation(db).delete_customer(customer_id)
    return customer
