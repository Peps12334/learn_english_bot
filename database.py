from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from confiq import DB_URL

engine = create_async_engine(DB_URL, echo=True)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def init_db():
    import models
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)