from .celery_conf import celery_app
import time, os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.models.document import Document, DocumentMetadata
from app.core.config import UPLOAD_DIR, DATABASE_URL, OPENAI_API_KEY
from app.services.chrome_client import get_chroma_client
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import pandas as pd
        


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

embedding_function = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
client = get_chroma_client()

@celery_app.task(name="tasks.digest_document")
def ingest_document(doc_id: int):
    db = SessionLocal()
    try:
        doc = db.query(Document).filter(Document.id == doc_id).first()
        if not doc:
            return f"Document {doc_id} not found"

        file_path = os.path.join(UPLOAD_DIR, doc.filename)
        if not os.path.exists(file_path):
            doc.current_status = 4
            db.commit()
            return f"File not found for doc_id {doc_id}"


        metadata = db.query(DocumentMetadata).filter_by(document_id=doc.id).all()
        metadata_dict = {entry.key: entry.value for entry in metadata}
        print(f"[Meta for Doc {doc_id}]: {metadata_dict}")


        # Read file content as plain text
        ext = os.path.splitext(doc.filename)[1].lower()
        if ext == ".csv":
            df = pd.read_csv(file_path)
            file_content = df.to_string()
        elif ext in [".xls", ".xlsx"]:
            df = pd.read_excel(file_path)
            file_content = df.to_string()
        else:
            file_content = open(file_path, "r", encoding="utf-8").read()

        embedding_vector = embedding_function.embed_documents([file_content])[0]

        chroma_collection = client.get_or_create_collection("documents")
        chroma_collection.add(
            embeddings=[embedding_vector],
            documents=[file_content],
            metadatas=[
                {"document_id": str(doc.id)}, 
                metadata_dict
            ],
            ids=[str(doc.id)]
        )

        doc.current_status = 3  # Ingest Completed
        db.commit()
        return f"Document {doc_id} digested successfully"
    except Exception as e:
        if doc:
            doc.current_status = 4
            db.commit()
        return f"Failed to digest document {doc_id}: {str(e)}"
    finally:
        db.close()