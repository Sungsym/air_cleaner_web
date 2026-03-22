from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlmodel import SQLModel, Session

from app.config import settings


db_url = settings.POSTGRES_URL
engine = create_async_engine(db_url, echo=True)

# 异步创建表
async def create_db_and_tables():
    async with engine.begin() as conn:
        from app.database.models import Air
        await conn.run_sync(SQLModel.metadata.create_all)

# 异步获取会话
async def get_session():
    async_session = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session



# # 同步代码
# from sqlalchemy import create_engine
# from sqlmodel import SQLModel, Session
# from app.config import settings


# db_url = settings.POSTGRES_URL
# engine = create_engine(db_url, echo=True)

# def create_db_and_tables():
#     from app.database.models import Air
#     SQLModel.metadata.create_all(engine)

# def get_session():
#     with Session(engine) as session:
#         yield session