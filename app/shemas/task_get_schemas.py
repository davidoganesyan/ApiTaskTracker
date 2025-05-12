from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    name: str
    surname: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class AssigneeResponse(BaseModel):
    user: UserResponse
    assignee_status: str

    model_config = ConfigDict(from_attributes=True)


class TaskResponse(BaseModel):
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
