from pydantic import BaseModel, ConfigDict


class AllUserResponse(BaseModel):
    id: int
    name: str
    surname: str
    email: str

    model_config = ConfigDict(
        from_attributes=True,
    )
