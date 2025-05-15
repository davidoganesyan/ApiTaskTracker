from pydantic import BaseModel, ConfigDict


class AllUserResponse(BaseModel):
    """Модель ответа с дополнительными данными пользователя.

    Attributes:
        id (int): Уникальный идентификатор пользователя
        name (str): Имя пользователя
        surname (str): Фамилия пользователя
        email (str): Адрес электронной почты
    """

    id: int
    name: str
    surname: str
    email: str

    model_config = ConfigDict(
        from_attributes=True,
    )
