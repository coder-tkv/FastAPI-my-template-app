# FastAPI My Template App

Шаблон FastAPI-приложения с примерами работы с PostgreSQL, Redis и кэшированием.
Все примеры можно удалить и оставить только нужную часть.

## Что внутри

- FastAPI + async SQLAlchemy + asyncpg
- Alembic для миграций
- Redis и примеры CRUD по ключам
- Кэширование через fastapi-cache2
- Docker Compose для локальной среды

## Быстрый старт (Docker)

1) Запустите все сервисы:

```bash
docker compose up --build
```

2) Откройте:
- API: http://localhost:8080
- Swagger: http://localhost:8080/docs

Docker-старт автоматически применяет миграции (см. `src/prestart.sh`).

## Локальный запуск

1) Подготовьте `.env` — скопируйте `src/.env.template` в `src/.env`.

2) Установите зависимости (если используете `uv`):

```bash
uv sync
```

3) Примените миграции:

```bash
cd src
alembic upgrade head
```

4) Запустите API:

```bash
cd src
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Примеры и эндпоинты

- `/users` — пример обычной работы с БД (SQLAlchemy)
- `/redis/*` — пример работы с Redis
- Кэширование списка пользователей через `@cache`

## Как удалить примеры

Все примеры независимы, можно вырезать только то, что не нужно.

### Убрать Redis пример полностью

- Удалить `src/api/redis_example.py`.
- Удалить импорт/подключение в `src/api/__init__.py`.
- Удалить `src/api/dependencies.py` и `src/utils/redis_key_builders.py` (если больше не нужны).
- Удалить Redis из `src/create_fastapi_app.py` (инициализация и закрытие соединения).
- Удалить Redis-конфиг из `src/config.py`.
- Удалить переменные `REDIS__*` из `.env` и `docker-compose.yaml`.
- Удалить сервис `redis` из `docker-compose.yaml`.
- Удалить зависимость `redis` из `pyproject.toml`.

### Убрать только кэширование

- В `src/api/users_example.py`:
  - Удалить декоратор `@cache`.
  - Удалить `FastAPICache.clear`.
- В `src/create_fastapi_app.py`:
  - Удалить `FastAPICache.init(...)`.
- Удалить зависимость `fastapi-cache2` из `pyproject.toml`.

### Убрать пример работы с БД

- Удалить `src/api/users_example.py` и отключить роутер в `src/api/__init__.py`.
- Удалить `src/crud/users.py`, `src/models/user.py`, `src/schemas/user.py`.
- Если БД вообще не нужна:
  - Удалить `src/database/db_helper.py`, `src/models/base.py`.
  - Удалить `db` конфиг из `src/config.py`.
  - Удалить зависимость `asyncpg`, `sqlalchemy` из `pyproject.toml`.
  - Удалить сервис `db` из `docker-compose.yaml`.

### Убрать пример миграции БД

Вариант 1 — убрать только демо-миграцию:
- Удалить файл `src/alembic/versions/2025_12_20_1924-45dc24e5bf22_demo_user_migration.py`.
- Если миграция уже применена к БД, сначала выполните:

```bash
cd src
alembic downgrade -1
```

Если миграция еще не применялась, можно просто удалить файл.
- Создать свою миграцию:

```bash
cd src
alembic revision --autogenerate -m "init"
```

Вариант 2 — полностью убрать Alembic:
- Удалить папку `src/alembic` и файл `src/alembic.ini`.
- Удалить зависимость: `uv remove alembic`.
- Удалить шаг миграций из `src/prestart.sh`.

## Структура проекта (коротко)

- `src/main.py` — точка входа FastAPI
- `src/create_fastapi_app.py` — создание приложения и middleware
- `src/api/*` — API-роуты (примеры)
- `src/models/*`, `src/crud/*`, `src/schemas/*` — пример работы с БД
- `src/alembic/*` — миграции
