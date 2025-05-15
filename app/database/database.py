from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    """Базовый класс для всех моделей SQLAlchemy.

    Наследует:
        - AsyncAttrs: Поддержка асинхронных операций
        - DeclarativeBase: Декларативный стиль SQLAlchemy
    """

    pass


engine = create_async_engine("sqlite+aiosqlite:///./app.db")

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Зависимость для инъекции асинхронной сессии БД.

    Создает новую сессию для каждого запроса и автоматически:
        - Фиксирует изменения при успешном выполнении
        - Откатывает при возникновении ошибок
        - Закрывает соединение

    Returns:
        AsyncSession: Асинхронная сессия SQLAlchemy

    Использование:
        db = Depends(get_db) в обработчиках FastAPI
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
