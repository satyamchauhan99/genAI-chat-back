import os
from fastapi import APIRouter, UploadFile, File
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.document_service import save_document, save_ingest_document, list_documents
from app.services.auth_service import get_current_user
from app.models.user import User
from app.models.document import Document, DocumentMetadata
from app.schemas.document import MetadataInput
from app.celery.tasks import ingest_document
from app.core.config import ALLOWED_EXTENSIONS, UPLOAD_DIR



router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload/")
async def upload_file(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)  # user object from token
):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="File type not allowed")

    filepath = os.path.join(UPLOAD_DIR, file.filename)
    with open(filepath, "wb") as f:
        while chunk := file.file.read(1024 * 1024):  # 1MB chunks
            f.write(chunk)

    doc = await save_document(db, file.filename, current_user.id)
    return {"doc_id": doc.id, "message": "File uploaded successfully"}


@router.post("/metadata/")
def save_metadata(data: MetadataInput, db: AsyncSession = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == data.document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    meta = DocumentMetadata(document_id=data.document_id, key=data.key, value=data.value)
    db.add(meta)
    db.commit()
    db.refresh(meta)
    return {"message": "Metadata saved", "metadata_id": meta.id}


@router.get("/ingest/{doc_id}")
def trigger_ingest(
        doc_id: int, 
        db: AsyncSession = Depends(get_db)
    ):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    doc.current_status = 2  # Ingest Triggered
    db.commit()
    
    ingest_document.delay(doc_id) # Function for Triggered
    return {"message": f"Ingestion triggered for doc_id {doc_id}"}



@router.post("/upload-and-ingest")
async def upload_document(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        content = (await file.read()).decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be UTF-8 encoded text.")

    doc = await save_ingest_document(db, file.filename, current_user.id, content)

    return {
        "message": "Document uploaded successfully",
        "document_id": doc.id,
        "uploaded_by": current_user.email
    }


@router.get("/list")
async def get_documents(db: AsyncSession = Depends(get_db)):
    documents = await list_documents(db)
    return documents
