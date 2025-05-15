from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class User(Base):
    """Модель пользователя с базовой информацией и связями задач.

    Attributes:
        id (int): Уникальный идентификатор пользователя
        name (str): Имя пользователя (до 30 символов)
        surname (str): Фамилия пользователя (до 50 символов)
        patronymic (str | None): Отчество (опционально, до 50 символов)
        email (str): Уникальный email (до 100 символов)
        position (str | None): Должность пользователя (опционально)
        created_tasks (List[Task]): Задачи, созданные пользователем
        assigned_tasks (List[TaskAssignee]): Задачи, назначенные пользователю
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    surname: Mapped[str] = mapped_column(String(50), nullable=False)
    patronymic: Mapped[str] = mapped_column(String(50), nullable=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    position: Mapped[str] = mapped_column(String(200), nullable=True)

    created_tasks: Mapped[List["Task"]] = relationship(back_populates="author", lazy="selectin")  # type: ignore # noqa
    assigned_tasks: Mapped[List["TaskAssignee"]] = relationship(back_populates="user", lazy="selectin")  # type: ignore # noqa
