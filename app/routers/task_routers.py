from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.routers.task_management import (
    create_task,
    delete_task,
    get_all_tasks,
    get_task_by_id,
    update_task,
)
from app.shemas.task_get_schemas import TaskResponse, TaskResponseById
from app.shemas.task_patch_schemas import TaskUpdate
from app.shemas.task_post_schemas import TaskCreate

router = APIRouter(prefix="/api")


@router.get("/tasks", response_model=List[TaskResponse])
async def read_tasks(db: AsyncSession = Depends(get_db)):  # noqa
    return await get_all_tasks(db)


@router.post("/tasks", response_model=TaskCreate, status_code=status.HTTP_201_CREATED)
async def create_new_task(
    task_data: TaskCreate, db: AsyncSession = Depends(get_db)  # noqa
):
    return await create_task(task_data, db)


@router.patch("/tasks/{task_id}", response_model=TaskUpdate)
async def update_existing_task(
    task_id: int, task_data: TaskUpdate, db: AsyncSession = Depends(get_db)
):
    return await update_task(task_id, task_data, db)


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_endpoint(task_id: int, db: AsyncSession = Depends(get_db)):
    await delete_task(task_id, db)
    return {"detail": "Task successfully deleted"}


@router.get("/tasks/{task_id}", response_model=TaskResponseById)
async def get_task_id(task_id: int, db: AsyncSession = Depends(get_db)):
    return await get_task_by_id(task_id, db)
