from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


from backend.authentication.authorization import get_current_active_user, is_admin_user
from backend.db.engine import get_db
from backend.operation.customer import CustomerOperation
from backend.schema.customer import (
    CustomerCreate,
    CustomerInDB,
    CustomerUpdate,
)
from backend.schema.user import UserInDB

router = APIRouter()


@router.get(
    "/customers",
)
async def api_read_all_customer(
    db: AsyncSession = Depends(get_db), current_user: UserInDB = Depends(is_admin_user)
):
    customers = await CustomerOperation(db).get_all_customers()
    return customers


@router.get("/customers/{user_id}")
async def api_get_customer_by_user_id(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    if user_id != current_user.id and current_user.user_type.value != "admin":
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "not allowed!")
    customer = await CustomerOperation(db).get_customer_by_user_id(user_id)
    return customer


@router.post("/customers", response_model=CustomerInDB)
async def api_create_customer(
    customer: CustomerCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    customer.user_id = current_user.id
    return await CustomerOperation(db).create_customer(customer)


@router.put("/customers/{customer_id}")
async def api_update_customer(
    customer_id: int,
    customer: CustomerUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    data = customer.dict()
    data.update({"user_id": current_user.id})
    customer = await CustomerOperation(db).update_customer(customer_id, data)
    return customer


@router.delete("/customer/{customer_id}")
async def api_delete_customer(
    customer_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserInDB = Depends(get_current_active_user),
):
    if current_user.user_type.value != "admin":
        data = {"user_id": current_user.id}
        customer = await CustomerOperation(db).delete_customer(customer_id, data)
        return customer
    else:
        customer = await CustomerOperation(db).force_delete_customer(customer_id)
        return customer
