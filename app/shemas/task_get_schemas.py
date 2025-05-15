from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    """Модель ответа с данными пользователя.

    Attributes:
        name (str): Имя пользователя
        surname (str): Фамилия пользователя
        email (str): Email пользователя
    """

    name: str
    surname: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class AssigneeResponse(BaseModel):
    """Модель связи пользователя с задачей.

    Attributes:
        user (UserResponse): Данные пользователя-исполнителя
        assignee_status (str): Статус исполнителя в задаче
    """

    user: UserResponse
    assignee_status: str

    model_config = ConfigDict(from_attributes=True)


class TaskResponse(BaseModel):
    """Полная модель задачи с вложенными данными.

    Attributes:
        id (int): Уникальный идентификатор задачи
        title (str): Название задачи
        description (str): Описание задачи
        parent_id (int | None): ID родительской задачи (если есть)
        children (list["TaskResponse"]): Список вложенных подзадач
        created_at (datetime): Дата создания (ISO 8601)
        end_date (datetime | None): Дата завершения (ISO 8601)
        author (UserResponse): Данные автора задачи
        status (str): Текущий статус задачи
        assignees (list[AssigneeResponse]): Список исполнителей

    Note:
        Даты сериализуются в формате "YYYY-MM-DD HH:MM"
    """

    id: int
    title: str
    description: str
    parent_id: int | None = None
    children: list["TaskResponse"] = []
    created_at: datetime
    end_date: datetime | None = None
    author: UserResponse
    status: str
    assignees: list[AssigneeResponse] = []

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={datetime: lambda v: v.strftime("%Y-%m-%d %H:%M")},
    )


class TaskResponseById(BaseModel):
    """Упрощенная модель задачи для отдельного запроса.

    Отличается от TaskResponse отсутствием:
    - status
    - children

    Attributes:
        id (int): Уникальный идентификатор задачи
        title (str): Название задачи
        description (str): Описание задачи
        parent_id (int | None): ID родительской задачи (если есть)
        created_at (datetime): Дата создания (ISO 8601)
        end_date (datetime | None): Дата завершения (ISO 8601)
        author (UserResponse): Данные автора задачи
        assignees (list[AssigneeResponse]): Список исполнителей

    Note:
        Даты сериализуются в формате "YYYY-MM-DD HH:MM"
    """

    id: int
    title: str
    description: str
    parent_id: int | None = None
    created_at: datetime
    end_date: datetime | None = None
    author: UserResponse
    assignees: list[AssigneeResponse] = []

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={datetime: lambda v: v.strftime("%Y-%m-%d %H:%M")},
    )
