from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    surname: Mapped[str] = mapped_column(String(50), nullable=False)
    patronymic: Mapped[str] = mapped_column(String(50), nullable=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    position: Mapped[str] = mapped_column(String(200), nullable=True)

    created_tasks: Mapped[List["Task"]] = relationship(back_populates="author", lazy="selectin")  # type: ignore # noqa
    assigned_tasks: Mapped[List["TaskAssignee"]] = relationship(back_populates="user", lazy="selectin")  # type: ignore # noqa
