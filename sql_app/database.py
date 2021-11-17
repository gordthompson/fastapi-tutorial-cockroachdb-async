from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = URL.create(
    "cockroachdb+asyncpg",
    username="root",
    host="localhost",
    port=26257,
    database="defaultdb",
    query={"disable_cockroachdb_telemetry": "True"}
)

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

Base = declarative_base()
