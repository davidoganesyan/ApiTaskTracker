from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tasks import Task, TaskAssignee
from app.models.users import User


async def populate_database(session: AsyncSession):
    users = [
        User(name="John", surname="Doe", email="john@example.com"),
        User(name="Maria", surname="Ivanova", email="maria@example.com"),
        User(name="Alex", surname="Smith", email="alex@example.com"),
    ]
    session.add_all(users)

    main_tasks = [
        Task(
            title="Test Task 1",
            description="Test Title 1",
            end_date=datetime(2025, 5, 20, 12, 30),
            author=users[0],
        ),
        Task(
            title="Test Task 2",
            description="Test Title 2",
            end_date=datetime(2025, 5, 20, 12, 30),
            author=users[0],
        ),
        Task(
            title="Test Task 3",
            description="Test Title 3",
            end_date=datetime(2025, 5, 20, 12, 30),
            author=users[0],
        ),
    ]
    session.add_all(main_tasks)

    subtasks = [
        Task(
            title="Sub Task 1",
            description="Sub Title 1",
            end_date=datetime(2025, 5, 20, 12, 30),
            author=users[1],
            parent=main_tasks[0],
        ),
        Task(
            title="Sub Task 2",
            description="Sub Title 2",
            end_date=datetime(2025, 5, 20, 12, 30),
            author=users[1],
            parent=main_tasks[1],
        ),
        Task(
            title="Sub Task 3",
            description="Sub Title 1",
            end_date=datetime(2025, 5, 20, 12, 30),
            author=users[1],
            parent=main_tasks[1],
        ),
    ]
    session.add_all(subtasks)

    subtasks_for_subtasks = [
        Task(
            title="Sub for Sub Task 1",
            description="Sub for Sub Title 1",
            end_date=datetime(2025, 5, 20, 12, 30),
            author=users[1],
            parent=subtasks[0],
        ),
    ]

    session.add_all(subtasks_for_subtasks)

    assignees = [
        TaskAssignee(user=users[1], task=main_tasks[0]),
        TaskAssignee(user=users[2], task=main_tasks[1]),
        TaskAssignee(user=users[0], task=subtasks[1]),
    ]
    session.add_all(assignees)

    await session.commit()
