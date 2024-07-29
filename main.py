from fastapi import FastAPI, status
from dotenv import load_dotenv

from backend.db.engine import engine, Base
from backend.router import user, customer, auth

app = FastAPI()


@app.on_event("startup")
async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root_path() -> dict:
    return {"massage": "hello world!", "status": status.HTTP_200_OK}


app.include_router(user.router)
app.include_router(customer.router)
app.include_router(auth.router)
