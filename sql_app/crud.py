from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from . import models, schemas


async def get_user(async_session: AsyncSession, user_id: int):
    result = await async_session.execute(
        select(models.User)
        .where(models.User.id == user_id)
        .options(selectinload(models.User.items))
    )
    return result.scalars().first()


async def get_user_by_email(async_session: AsyncSession, email: str):
    result = await async_session.execute(
        select(models.User)
        .where(models.User.email == email)
        .options(selectinload(models.User.items))
    )
    return result.scalars().first()


async def get_users(
    async_session: AsyncSession, skip: int = 0, limit: int = 100
):
    result = await async_session.execute(
        select(models.User)
        .order_by(models.User.id)
        .offset(skip)
        .limit(limit)
        .options(selectinload(models.User.items))
    )
    return result.scalars().fetchall()


async def create_user(async_session: AsyncSession, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    new_user = models.User(
        email=user.email,
        hashed_password=fake_hashed_password,
        items=[],  # so pydantic won't trigger a lazy load
    )
    async_session.add(new_user)
    await async_session.commit()
    return new_user


async def get_items(
    async_session: AsyncSession, skip: int = 0, limit: int = 100
):
    result = await async_session.execute(
        select(models.Item)
        .order_by(models.Item.id)
        .offset(skip)
        .limit(limit)
        .options(selectinload(models.Item.owner))
    )
    return result.scalars().fetchall()


async def create_user_item(
    async_session: AsyncSession, item: schemas.ItemCreate, user_id: int
):
    new_item = models.Item(**item.dict(), owner_id=user_id)
    async_session.add(new_item)
    await async_session.commit()
    return new_item
