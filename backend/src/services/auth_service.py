"""Authentication service for the Todo application."""

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import Optional
from ..models.user import User, UserCreate
from ..auth import verify_password, get_password_hash
from datetime import timedelta


async def authenticate_user(session: AsyncSession, email: str, password: str) -> Optional[User]:
    """
    Authenticate a user by email and password.
    """
    # Find user by email
    statement = select(User).where(User.email == email)
    result = await session.execute(statement)
    user = result.first()

    if user is None:
        return None

    user = user[0] if isinstance(user, tuple) else user

    # Verify password
    if not verify_password(password, user.password_hash):
        return None

    return user


async def create_user(session: AsyncSession, user_create: UserCreate) -> User:
    """
    Create a new user with hashed password.
    """
    # Hash the password
    hashed_password = get_password_hash(user_create.password)

    # Create user instance
    user = User(
        email=user_create.email,
        name=user_create.name,
        password_hash=hashed_password
    )

    # Add to session and commit
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create an access token (wrapper for auth module function).
    """
    from ..auth import create_access_token as create_jwt_token
    return create_jwt_token(data, expires_delta)


async def create_user(session: AsyncSession, user_create: UserCreate) -> User:
    """
    Create a new user with hashed password.
    """
    # Hash the password
    hashed_password = get_password_hash(user_create.password)

    # Create user instance
    user = User(
        email=user_create.email,
        name=user_create.name,
        password_hash=hashed_password
    )

    # Add to session and commit
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user