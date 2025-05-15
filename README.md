# Task Tracker

## Описание проекта
API сервис для управления задачами с использованием FastAPI + JS. Позволяет пользователям создавать, просматривать, обновлять и удалять задачи

## Технологии
- **FastAPI** - веб-фреймворк
- **SQLite** - база данных
- **SQLAlchemy** - ORM для работы с БД
- **Alembic** - управление миграциями
- **JS** - фронтед


## Установка и запуск

### Предварительные требования
1. Python 3.12

### Запуск проекта
1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com/davidoganesyan/ApiTaskTracker.git
2. Установите зависимости
   ```bash
   pip install -r requirements.txt
3. Примените начальную миграцию
   ```bash
   alembic upgrade head

4. Запустите сервер
   ```bash
   uvicorn main:app

## Дерево задач доступно по адресу
http://localhost:8000/static/
## Документация API
Swagger UI : http://localhost:8000/docs