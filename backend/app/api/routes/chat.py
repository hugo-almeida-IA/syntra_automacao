from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.ai.ollama_main import gerar_resposta
from app.core.enums.papel_mensagem import PapelMensagem
from app.database.session import get_db
from app.services.cliente_service import buscar_ou_criar_cliente
from app.services.conversa_service import buscar_ou_criar_conversa
from app.services.mensagem_service import (
    buscar_historico,
    criar_mensagem,
)


router = APIRouter()


class RequisicaoChat(BaseModel):
    telefone: str
    prompt: str


@router.post("/chat")
async def resposta(
    dados: RequisicaoChat,
    db: Session = Depends(get_db),
):
    cliente = buscar_ou_criar_cliente(
        db=db,
        telefone=dados.telefone,
    )

    conversa = buscar_ou_criar_conversa(
        db=db,
        cliente=cliente,
    )

    historico = buscar_historico(
        db=db,
        conversa=conversa,
    )

    historico_ollama = [
        {
            "role": mensagem.papel,
            "content": mensagem.conteudo,
        }
        for mensagem in historico
    ]

    criar_mensagem(
        db=db,
        conversa=conversa,
        conteudo=dados.prompt,
        papel=PapelMensagem.USER,
    )

    resposta_llm = await gerar_resposta(
        prompt=dados.prompt,
        historico=historico_ollama,
    )

    criar_mensagem(
        db=db,
        conversa=conversa,
        conteudo=resposta_llm,
        papel=PapelMensagem.ASSISTANT,
    )

    db.commit()

    return {"Texto LLM": resposta_llm}