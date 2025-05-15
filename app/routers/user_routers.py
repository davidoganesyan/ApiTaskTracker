from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only

from app.database.database import get_db
from app.models.users import User
from app.shemas.user_schemas import AllUserResponse

router = APIRouter(prefix="/api")


@router.get("/users", response_model=list[AllUserResponse])
async def get_users(db: AsyncSession = Depends(get_db)) -> list[AllUserResponse]:
    """Получить список пользователей с базовой информацией

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy

    Returns:
        list[AllUserResponse]: Список пользователей с основными полями:
            - id (int)
            - name (str)
            - surname (str)
            - email (str)

    Status Codes:
        200 OK: Успешный ответ
    """
    stmt = select(User).options(load_only(User.id, User.name, User.surname, User.email))
    result = await db.execute(stmt)
    users = result.scalars().all()
    return [AllUserResponse.model_validate(user) for user in users]
