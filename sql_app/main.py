from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import async_engine, SessionLocal

app = FastAPI()


@app.on_event("startup")
async def db_setup():
    async with async_engine.begin() as conn:
        # await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)


# Dependency
async def get_async_session():
    async_session = SessionLocal()
    try:
        yield async_session
    finally:
        await async_session.close()


@app.post("/users/", response_model=schemas.User)
async def create_user(
    user: schemas.UserCreate,
    async_session: AsyncSession = Depends(get_async_session),
):
    existing_user = await crud.get_user_by_email(
        async_session, email=user.email
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = await crud.create_user(async_session=async_session, user=user)
    return new_user


@app.get("/users/", response_model=List[schemas.User])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    async_session: AsyncSession = Depends(get_async_session),
):
    users = await crud.get_users(async_session, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
async def read_user(
    user_id: int, async_session: AsyncSession = Depends(get_async_session)
):
    the_user = await crud.get_user(async_session, user_id=user_id)
    if the_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return the_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
async def create_item_for_user(
    user_id: int,
    item: schemas.ItemCreate,
    async_session: Session = Depends(get_async_session),
):
    return await crud.create_user_item(
        async_session=async_session, item=item, user_id=user_id
    )


@app.get("/items/", response_model=List[schemas.Item])
async def read_items(
    skip: int = 0,
    limit: int = 100,
    async_session: Session = Depends(get_async_session),
):
    items = await crud.get_items(async_session, skip=skip, limit=limit)
    return items
