from fastapi import APIRouter
from pydantic import BaseModel

from app.ai.ollama_main import gerar_resposta


router = APIRouter()


class RequisicaoChat(BaseModel):
    prompt: str


@router.post("/chat")
async def resposta(dados: RequisicaoChat):
    resposta_llm = await gerar_resposta(dados.prompt)

    return {"Texto LLM": resposta_llm}