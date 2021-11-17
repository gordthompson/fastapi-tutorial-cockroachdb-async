from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from . import models, schemas


async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(models.User)
        .where(models.User.id == user_id)
        .options(selectinload(models.User.items))
    )
    return result.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(
        select(models.User)
        .where(models.User.email == email)
        .options(selectinload(models.User.items))
    )
    return result.scalars().first()


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(models.User)
        .order_by(models.User.id)
        .offset(skip)
        .limit(limit)
        .options(selectinload(models.User.items))
    )
    return result.scalars().fetchall()


async def create_user(db: AsyncSession, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        email=user.email,
        hashed_password=fake_hashed_password,
        items=[],  # so pydantic won't trigger a lazy load
    )
    db.add(db_user)
    await db.commit()
    return db_user


async def get_items(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(models.Item)
        .order_by(models.Item.id)
        .offset(skip)
        .limit(limit)
        .options(selectinload(models.Item.owner))
    )
    return result.scalars().fetchall()


async def create_user_item(
    db: AsyncSession, item: schemas.ItemCreate, user_id: int
):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    await db.commit()
    return db_item
