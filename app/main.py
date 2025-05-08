# app/main.py
from fastapi import FastAPI
from app.api import auth, document, qa
from app.models.user import Base as UserBase
from app.models.document import Base as DocumentBase
from app.database import engine

app = FastAPI()

app.include_router(auth.router)
app.include_router(document.router)
app.include_router(qa.router)

# Create DB tables
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(UserBase.metadata.create_all)
        await conn.run_sync(DocumentBase.metadata.create_all)
