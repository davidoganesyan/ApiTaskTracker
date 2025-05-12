from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only

from app.database.database import get_db
from app.models.users import User
from app.shemas.user_schemas import AllUserResponse

router = APIRouter(prefix="/api")


@router.get("/users", response_model=List[AllUserResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    stmt = select(User).options(
        load_only(User.id, User.name, User.surname, User.email)  # Явно указываем поля
    )
    result = await db.execute(stmt)
    users = result.scalars().all()
    return [AllUserResponse.model_validate(user) for user in users]
