"""Database engine and session management for the Todo application."""

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from .config import settings


# Create async engine
async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO  # Set to True for debugging SQL queries
)

# Create async session maker
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_async_session():
    """Dependency to get async database session."""
    async with AsyncSessionLocal() as session:
        yield session