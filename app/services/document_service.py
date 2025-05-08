import os
from sqlalchemy.future import select
from app.models.document import Document
from app.core.config import OPENAI_API_KEY
from app.services.chrome_client import get_chroma_client
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma


embedding_function = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
client = get_chroma_client()

async def save_document(db, filename: str, user_id: int):
    doc = Document(filename=filename, current_status=1, user_id=user_id)
    db.add(doc)
    await db.commit()
    await db.refresh(doc)

async def save_ingest_document(db, filename: str, user_id: int, file_content: str):
    doc = Document(filename=filename, current_status=1, user_id=user_id)
    db.add(doc)
    await db.commit()
    await db.refresh(doc)
    embedding_vector = embedding_function.embed_documents([file_content])[0]
    chroma_collection = client.get_or_create_collection("documents")
    chroma_collection.add(
        embeddings=[embedding_vector],
        documents=[file_content],
        metadatas=[{"document_id": str(doc.id)}], # Assuming user is giving metadata in same request 
        ids=[str(doc.id)]
    )
    return doc

async def list_documents(db):
    result = await db.execute(select(Document))
    documents = result.scalars().all()
    return documents
