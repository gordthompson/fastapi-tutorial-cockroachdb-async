from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

# Comment/Uncomment the following two blocks and adjust as needed
#
# =========================================================
# Option 1: asyncpg
# ---------------------------------------------------------
SQLALCHEMY_DATABASE_URL = URL.create(
    "cockroachdb+asyncpg",
    username="root",
    host="localhost",
    port=26257,
    database="defaultdb",
)
async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    isolation_level="SERIALIZABLE",
)
# ---------------------------------------------------------

# ========================================================
# Option 2: psycopg
# --------------------------------------------------------
# import psycopg
#
#
# async def get_async_crdb_connection():
#     return await psycopg.crdb.AsyncCrdbConnection.connect(
#         "host=localhost "
#         "port=26257 "
#         "user=root "
#         "dbname=defaultdb"
#     )
#
#
# async_engine = create_async_engine(
#     "cockroachdb+psycopg://",
#     async_creator=get_async_crdb_connection,
# )
# --------------------------------------------------------

SessionLocal = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()
