from datetime import datetime
from typing import List

from sqlalchemy import TIMESTAMP, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class Task(Base):
    """Модель задачи с поддержкой вложенности и связями с пользователями.

    Attributes:
        id (int): Уникальный идентификатор задачи
        title (str): Заголовок задачи (до 50 символов)
        description (str): Подробное описание задачи (до 500 символов)
        created_at (datetime): Время создания (автоматическое)
        end_date (datetime): Срок выполнения
        status (str): Статус задачи (по умолчанию 'pending')
        parent_id (int | None): ID родительской задачи (если есть)
        parent (Task | None): Родительская задача
        children (List[Task]): Список подзадач
        author (User): Пользователь-создатель задачи
        assignees (List[TaskAssignee]): Список назначенных исполнителей
    """

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    end_date: Mapped[datetime | None] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False
    )
    status: Mapped[str] = mapped_column(String(50), default="pending")

    parent_id: Mapped[int | None] = mapped_column(ForeignKey("tasks.id"))
    parent: Mapped["Task | None"] = relationship(
        "Task", remote_side=[id], back_populates="children", lazy="selectin"
    )
    children: Mapped[List["Task"]] = relationship(
        "Task", back_populates="parent", lazy="selectin", cascade="all, delete"
    )

    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship(back_populates="created_tasks", lazy="selectin")  # type: ignore # noqa

    assignees: Mapped[List["TaskAssignee"]] = relationship(
        back_populates="task", lazy="selectin", cascade="all, delete"
    )


class TaskAssignee(Base):
    """Связующая модель для назначения задач пользователям.

    Attributes:
        user_id (int): ID пользователя
        task_id (int): ID задачи
        assignee_status (str): Статус назначения (по умолчанию 'pending')
        assigned_at (datetime): Время назначения (автоматическое)
        user (User): Связанный пользователь
        task (Task): Связанная задача
    """

    __tablename__ = "task_assignees"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), primary_key=True)
    assignee_status: Mapped[str] = mapped_column(String(50), default="pending")
    assigned_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="assigned_tasks", lazy="selectin")  # type: ignore # noqa
    task: Mapped["Task"] = relationship(back_populates="assignees", lazy="selectin")
