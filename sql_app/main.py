from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import engine, SessionLocal

app = FastAPI()


@app.on_event("startup")
async def db_setup():
    async with engine.begin() as conn:
        # await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)


# Dependency
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


@app.post("/users/", response_model=schemas.User)
async def create_user(
    user: schemas.UserCreate, db: AsyncSession = Depends(get_db)
):
    existing_user = await crud.get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = await crud.create_user(db=db, user=user)
    return new_user


@app.get("/users/", response_model=List[schemas.User])
async def read_users(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    users = await crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    the_user = await crud.get_user(db, user_id=user_id)
    if the_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return the_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
async def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return await crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=List[schemas.Item])
async def read_items(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    items = await crud.get_items(db, skip=skip, limit=limit)
    return items
