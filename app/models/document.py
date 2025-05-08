from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    current_status = Column(Integer, default=1)  # 1: Just Uploaded, 2. Trigger Indigest 3. Indigest Completed 4. Failed
    user_id = Column(Integer, ForeignKey("users.id"))

    metadata_entries = relationship("DocumentMetadata", back_populates="document", cascade="all, delete")



class DocumentMetadata(Base):
    __tablename__ = "document_metadata"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"))
    key = Column(String, nullable=False)
    value = Column(String, nullable=False)

    document = relationship("Document", back_populates="metadata_entries")
