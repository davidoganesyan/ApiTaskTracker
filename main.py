from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database.utils import init_data
from app.routers import task_routers, user_routers


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Управляет жизненным циклом приложения.

    Выполняет инициализацию данных при старте приложения.
    """
    await init_data()
    yield


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static", html=True), name="static")

app.include_router(task_routers.router)
app.include_router(user_routers.router)
