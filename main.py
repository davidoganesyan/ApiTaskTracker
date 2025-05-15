from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database.database import AsyncSessionLocal, Base, engine
from app.database.utils import init_data, populate_database
from app.routers import task_routers, user_routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_data()
    yield

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # async with engine.begin() as conn:
#         # await conn.run_sync(Base.metadata.drop_all)
#         # await conn.run_sync(Base.metadata.create_all)
#     async with AsyncSessionLocal() as session:
#         await populate_database(session)
#     yield


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static", html=True), name="static")

app.include_router(task_routers.router)
app.include_router(user_routers.router)
