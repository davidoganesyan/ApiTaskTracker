from datetime import datetime
from typing import List

from sqlalchemy import TIMESTAMP, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class Task(Base):
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
    __tablename__ = "task_assignees"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), primary_key=True)
    assignee_status: Mapped[str] = mapped_column(String(50), default="pending")
    assigned_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="assigned_tasks", lazy="selectin")  # type: ignore # noqa
    task: Mapped["Task"] = relationship(back_populates="assignees", lazy="selectin")
