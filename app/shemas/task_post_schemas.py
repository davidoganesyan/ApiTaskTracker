from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TaskCreate(BaseModel):
    """Модель для создания новой задачи.

    Обязательные поля:
    - title
    - description
    - end_date
    - author_id

    Attributes:
        title (str): Название задачи
        description (str): Подробное описание задачи
        end_date (datetime): Срок выполнения (YYYY-MM-DD HH:mm)
        parent_id (int | None): ID родительской задачи (для подзадач)
        author_id (int): ID пользователя-автора задачи
        assignee_user_ids (list[int]): Список ID исполнителей (по умолчанию пустой)

    Note:
        Для end_date используйте формат "YYYY-MM-DD HH:mm"
        Пример тела запроса доступен в конфигурации модели
    """

    title: str
    description: str
    end_date: datetime = Field(json_schema_extra={"format": "YYYY-MM-DD HH:mm"})
    parent_id: int | None = None
    author_id: int
    assignee_user_ids: list[int] | None = Field(default_factory=list)  # type: ignore

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={datetime: lambda v: v.strftime("%Y-%m-%d %H:%M")},
        json_schema_extra={
            "example": {
                "title": "New Task",
                "description": "Description here",
                "end_date": "2025-05-30 15:40",
                "parent_id": 1,
                "author_id": 1,
                "assignee_user_ids": [2, 3],
            }
        },
    )
