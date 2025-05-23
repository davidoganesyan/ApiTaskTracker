from fastapi import HTTPException
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.tasks import Task, TaskAssignee
from app.models.users import User
from app.shemas.task_patch_schemas import TaskUpdate
from app.shemas.task_post_schemas import TaskCreate


async def get_task_by_id(task_id: int, session: AsyncSession) -> Task | None:
    """Получить задачу по ID с полными связями

    Args:
        task_id (int): ID запрашиваемой задачи
        session (AsyncSession): Асинхронная сессия SQLAlchemy

    Returns:
        Task | None: Задача с автором и списком назначенных пользователей, или None если не найдена
    """
    task = await session.execute(
        select(Task)
        .options(
            selectinload(Task.author),
            selectinload(Task.assignees).selectinload(TaskAssignee.user),
        )
        .where(Task.id == task_id)
    )
    return task.scalars().first()


async def get_all_tasks(session: AsyncSession) -> list[Task]:
    """Получить список корневых задач с подзадачами

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy

    Returns:
        List[Task]: Список задач с подзадачами, авторами и назначенными пользователями
    """
    result = await session.execute(
        select(Task).options(
            selectinload(Task.children),
            selectinload(Task.author),
            selectinload(Task.assignees).selectinload(TaskAssignee.user),
        )
    )

    all_tasks = result.scalars().all()
    finale_tasks = [task for task in all_tasks if task.parent_id is None]

    return finale_tasks


async def create_task(task_data: TaskCreate, session: AsyncSession) -> Task:
    """Создать новую задачу

    Args:
        task_data (TaskCreate): Данные для создания задачи
        session (AsyncSession): Асинхронная сессия SQLAlchemy

    Returns:
        Task: Созданная задача

    Raises:
        HTTPException(404): Если автор не найден
    """
    author = await session.get(User, task_data.author_id)
    if not author:
        raise HTTPException(status_code=404, detail="User not found")

    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        end_date=task_data.end_date,
        parent_id=task_data.parent_id,
        author_id=task_data.author_id,
    )

    session.add(new_task)
    await session.flush()

    assignees = [
        TaskAssignee(task_id=new_task.id, user_id=user_id)
        for user_id in task_data.assignee_user_ids  # type: ignore
    ]

    session.add_all(assignees)
    await session.commit()
    return new_task


async def update_task(
    task_id: int, task_data: TaskUpdate, session: AsyncSession
) -> Task:
    """Частично обновить задачу

    Args:
        task_id (int): ID обновляемой задачи
        task_data (TaskUpdate): Поля для изменения
        session (AsyncSession): Асинхронная сессия SQLAlchemy

    Returns:
        Task: Обновлённая задача

    Raises:
        HTTPException(404): Если задача не найдена
    """
    task = await get_task_by_id(task_id, session)

    if not task:
        raise HTTPException(404, detail="Task not found")

    for field, value in task_data.model_dump(exclude_unset=True).items():
        setattr(task, field, value)

    if task_data.assignee_user_ids:
        await session.execute(
            delete(TaskAssignee).where(TaskAssignee.task_id == task_id)
        )
        new_assignees = [
            TaskAssignee(task_id=task_id, user_id=user_id)
            for user_id in task_data.assignee_user_ids  # type: ignore
        ]
        session.add_all(new_assignees)

    await session.commit()
    return task


async def delete_task(task_id: int, session: AsyncSession) -> None:
    """Удалить задачу и все её подзадачи

    Args:
        task_id (int): ID удаляемой задачи
        session (AsyncSession): Асинхронная сессия SQLAlchemy

    Raises:
        HTTPException(404): Если задача не найдена
    """
    task = await session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await session.delete(task)
    await session.commit()
