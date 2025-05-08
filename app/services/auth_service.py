from passlib.context import CryptContext
from sqlalchemy.future import select
from app.models.user import User
from app.core.security import create_access_token
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends
from app.models.user import User
from jose import JWTError, jwt
from app.core.config import JWT_SECRET_KEY, JWT_ALGORITHM
from sqlalchemy.future import select
from app.database import get_db


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def authenticate_user(db, email: str, password: str):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    if user and verify_password(password, user.hashed_password):
        return user
    return None

async def create_user(db, email: str, password: str):
    hashed_password = get_password_hash(password)
    new_user = User(email=email, hashed_password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user



async def get_user_by_email(
        db: AsyncSession,
        email: str
    ):
    result = await db.execute(select(User).filter_by(email=email))
    user = result.scalars().first()  # Get the first matching user
    return user

async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)
    ):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication")

    user = await get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
