from fastapi import APIRouter
from pydantic import BaseModel, ValidationError
router = APIRouter()
class RequisicaoChat(BaseModel):
    prompt: str

@router.post("/chat")
def commit():
    return None