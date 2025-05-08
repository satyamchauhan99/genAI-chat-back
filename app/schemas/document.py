from pydantic import BaseModel

class MetadataInput(BaseModel):
    document_id: int
    key: str
    value: str

