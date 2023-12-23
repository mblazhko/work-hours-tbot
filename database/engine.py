from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, \
    async_sessionmaker

from config import DB_CONNECTION_URL

engine = create_async_engine(
    DB_CONNECTION_URL,
    echo=True,
    future=True,
)


async def get_session() -> AsyncSession:
    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    return async_session()
