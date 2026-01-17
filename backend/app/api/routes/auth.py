from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import create_access_token, get_password_hash, verify_password
from app.infrastructure.database.models import User, get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Any

router = APIRouter()

class RegisterRequest(BaseModel):
    username: str
    password: str

@router.post("/register")
async def register(request: RegisterRequest, db: AsyncSession = Depends(get_db)) -> Any:
    """Register a new user"""
    # Check if user already exists
    result = await db.execute(select(User).where(User.username == request.username))
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    # Hash the password
    hashed_password = get_password_hash(request.password)
    
    # Create new user
    new_user = User(
        username=request.username,
        hashed_password=hashed_password
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return {"message": "User registered successfully", "username": new_user.username}

@router.post("/token")
async def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
) -> Any:
    # Query user from database
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    # Verify password
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    # Create access token
    access_token = create_access_token(subject=user.username)
    return {"access_token": access_token, "token_type": "bearer"}
