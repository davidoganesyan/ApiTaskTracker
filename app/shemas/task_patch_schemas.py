from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TaskUpdate(BaseModel):
    """Модель для обновления задачи.

    Позволяет частичное обновление полей задачи. Все поля опциональны.

    Attributes:
        title (str | None): Новое название задачи
        description (str | None): Новое описание задачи
        end_date (datetime | None): Обновленный срок завершения (YYYY-MM-DD HH:mm)
        status (str | None): Новый статус задачи
        parent_id (int | None): Новый ID родительской задачи (или None)
        assignee_user_ids (list[int] | None): Список ID пользователей-исполнителей

    Note:
        Для end_date используйте формат "YYYY-MM-DD HH:mm"
        Пример тела запроса доступен в конфигурации модели
    """

    title: str | None = None
    description: str | None = None
    end_date: datetime | None = Field(
        None, json_schema_extra={"format": "YYYY-MM-DD HH:mm"}
    )
    status: str | None = None
    parent_id: int | None = None
    assignee_user_ids: list[int] | None = None

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={datetime: lambda v: v.strftime("%Y-%m-%d %H:%M")},
        json_schema_extra={
            "example": {
                "title": "Updated Task",
                "description": "New description",
                "end_date": "2025-05-30 16:00",
                "status": "in_progress",
                "parent_id": 2,
                "assignee_user_ids": [1, 3],
            }
        },
    )
