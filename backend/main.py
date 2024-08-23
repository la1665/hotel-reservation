from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from starlette.requests import Request
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from db.engine import engine
from db.models import Base
from router import user, auth
from exception_handeler.exceptions import (
    NotFoundException,
    NotAllowedException,
    UnauthorizedException,
    BadRequestExceptions,
)

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    # Shutdown logic (if needed)
    await engine.dispose()


app.router.lifespan_context = lifespan

# @app.on_event("startup")
# async def init_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root_path() -> dict:
    return {"massage": "hello world!", "status": status.HTTP_200_OK}


@app.exception_handler(NotAllowedException)
async def not_allowed_exception_handeler(request: Request, exc: NotAllowedException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": f"Custom Exception: {exc.name}", "details": exc.detail},
    )


@app.exception_handler(UnauthorizedException)
async def unauthorized_exception_handeler(request: Request, exc: UnauthorizedException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": f"Custom Exception: {exc.name}", "details": exc.detail},
        headers=exc.headers,
    )


@app.exception_handler(NotFoundException)
async def not_found_exception_handeler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": f"{exc.resource} not found!"},
    )


@app.exception_handler(BadRequestExceptions)
async def bad_request_exception_handeler(request: Request, exc: BadRequestExceptions):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"message": exc.detail}
    )


app.include_router(user.router)
app.include_router(auth.router)
