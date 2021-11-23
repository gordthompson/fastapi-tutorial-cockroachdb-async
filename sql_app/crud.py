from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from . import models, schemas


def hash_password(pwd):
    return pwd + "_NotReallyHashed"


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
    hashed_password = hash_password(user.password)
    new_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        items=[],  # so pydantic won't trigger a lazy load
    )
    async_session.add(new_user)
    await async_session.commit()
    return new_user


async def update_user(
    async_session: AsyncSession, user_id: int, user_info: schemas.UserUpdate
):
    results = await async_session.execute(
        select(models.User)
        .where(models.User.id == user_id)
        .options(selectinload(models.User.items))
    )
    the_user = results.scalar()
    if the_user is None:
        return None
    new_password = user_info.__dict__["password"]
    hashed_password = (
        hash_password(new_password)
        if new_password
        else the_user.hashed_password
    )
    for k, v in user_info.__dict__.items():
        if k == "password":
            setattr(the_user, "hashed_password", hashed_password)
        else:
            setattr(the_user, k, v)
    await async_session.commit()
    return the_user


async def delete_user(async_session: AsyncSession, user_id: int):
    the_user = await async_session.get(models.User, user_id)
    if the_user is None:
        return None
    await async_session.delete(the_user)
    await async_session.commit()
    return user_id


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
