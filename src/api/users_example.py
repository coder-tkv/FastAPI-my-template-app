from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_cache.decorator import cache

from config import settings
from database.db_helper import db_helper
from schemas.user import UserRead, UserCreate
from crud import users as users_crud
from utils.redis_key_builders import users_list_key_builder

router = APIRouter(prefix='/users', tags=["Users"])


@router.get("", response_model=list[UserRead])
@cache(expire=60, key_builder=users_list_key_builder, namespace=settings.cache.namespace.users_list)
async def get_users(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_session),
    ],
):
    users = await users_crud.get_all_users(session=session)
    return users


@router.post("", response_model=UserRead)
async def create_user(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.get_session),
    ],
    user_create: UserCreate,
):
    user = await users_crud.create_user(
        session=session,
        user_create=user_create,
    )
    return user
