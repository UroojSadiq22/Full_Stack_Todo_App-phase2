"""Authentication router for the Todo application."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import Optional
from datetime import timedelta
from ..models.user import User, UserCreate, UserResponse
from ..services.auth_service import authenticate_user, create_access_token, create_user
from ..database.session import get_async_session
from sqlmodel.ext.asyncio.session import AsyncSession
from ..utils.errors import DuplicateEmailException


router = APIRouter()
security = HTTPBearer()


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/token", response_model=Token)
async def login_for_access_token(
    user_credentials: UserCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = await authenticate_user(
        session, user_credentials.email, user_credentials.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)  # 30 minutes
    # Use user.id in the token instead of email
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserResponse)
async def register_user(
    user: UserCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Register a new user.
    """
    try:
        # Create new user using the auth service
        created_user = await create_user(session, user)
        return created_user
    except Exception as e:
        # Check if it's a duplicate email error
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )