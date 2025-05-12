from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TaskUpdate(BaseModel):
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
