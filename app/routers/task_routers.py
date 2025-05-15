from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.models.tasks import Task
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


@router.get("/tasks", response_model=list[TaskResponse])
async def read_tasks(db: AsyncSession = Depends(get_db)) -> list[Task]:
    """Получить список корневых задач с подзадачами

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy

    Returns:
        list[TaskResponse]: Список задач с подзадачами, автором и исполнителями

    Status Codes:
        200 OK: Успешный ответ
    """
    return await get_all_tasks(db)


@router.post("/tasks", response_model=TaskCreate, status_code=status.HTTP_201_CREATED)
async def create_new_task(
    task_data: TaskCreate, db: AsyncSession = Depends(get_db)
) -> Task:
    """Создать новую задачу

    Args:
        task_data (TaskCreate): Данные для создания задачи
        db (AsyncSession): Асинхронная сессия SQLAlchemy

    Returns:
        TaskCreate: Созданная задача в формате Pydantic-схемы

    Status Codes:
        201 Created: Успешное создание
        404 Not Found: Автор не найден
    """
    return await create_task(task_data, db)


@router.patch("/tasks/{id}", response_model=TaskUpdate)
async def update_existing_task(
    id: int, task_data: TaskUpdate, db: AsyncSession = Depends(get_db)
) -> Task:
    """Частично обновить задачу

    Args:
        id (int): ID обновляемой задачи
        task_data (TaskUpdate): Поля для изменения
        db (AsyncSession): Асинхронная сессия SQLAlchemy

    Returns:
        TaskUpdate: Обновлённая задача в формате Pydantic-схемы

    Status Codes:
        200 OK: Успешное обновление
        404 Not Found: Задача не найдена
    """
    return await update_task(id, task_data, db)


@router.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_endpoint(id: int, db: AsyncSession = Depends(get_db)) -> None:
    """Удалить задачу и все вложенные подзадачи

    Args:
        id (int): ID удаляемой задачи
        db (AsyncSession): Асинхронная сессия SQLAlchemy

    Status Codes:
        204 No Content: Успешное удаление
        404 Not Found: Задача не найдена
    """
    await delete_task(id, db)


@router.get("/tasks/{id}", response_model=TaskResponseById)
async def get_task_id(id: int, db: AsyncSession = Depends(get_db)) -> Task | None:
    """Получить задачу с подробной информацией

    Args:
        id (int): ID запрашиваемой задачи
        db (AsyncSession): Асинхронная сессия SQLAlchemy

    Returns:
        TaskResponseById: Полные данные задачи

    Status Codes:
        200 OK: Успешный ответ
        404 Not Found: Задача не найдена
    """
    return await get_task_by_id(id, db)
