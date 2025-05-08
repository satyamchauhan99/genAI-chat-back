from fastapi import APIRouter, Depends
from app.schemas.qa import QuestionRequest
from app.services.qa_service import ask_question
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/qa", tags=["qa"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/ask")
async def ask_qa(request: QuestionRequest, token: str = Depends(oauth2_scheme)):
    answer = ask_question(request.question, request.document_ids)
    return {"answer": answer}
