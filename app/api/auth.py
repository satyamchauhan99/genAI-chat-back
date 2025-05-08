from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.auth import UserCreate, Token
from app.services.auth_service import create_user, authenticate_user
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=Token)
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = await create_user(db, user.email, user.password)
    access_token = create_access_token(data={"sub": new_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
async def login(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}
