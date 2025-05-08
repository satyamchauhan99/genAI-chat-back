from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base 
from app.core.config import DATABASE_URL

Base = declarative_base()

engine = create_async_engine(DATABASE_URL, future=True, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
print("DBSesion**********-------------->", async_session)

async def get_db():
    async with async_session() as session:
        yield session
