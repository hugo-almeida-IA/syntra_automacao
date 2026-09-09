from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
import logging
import re

from pydantic import BaseModel, Field, field_validator
from app.core.config import settings

from fastapi import APIRouter, Depends, HTTPException

from app.ai.ollama_main import OllamaIndisponivelError, gerar_resposta
from app.core.enums.papel_mensagem import PapelMensagem
from app.database.session import get_db
from app.services.cliente_service import buscar_ou_criar_cliente
from app.services.conversa_service import buscar_ou_criar_conversa
from app.services.mensagem_service import (
    buscar_historico,
    criar_mensagem,
)


router = APIRouter()

logger = logging.getLogger(__name__)


class RequisicaoChat(BaseModel):
    telefone: str = Field(min_length=1, max_length=30)
    prompt: str = Field(min_length=1, max_length=4000)
    instancia: str = Field(default="local", min_length=1, max_length=100)

    @field_validator("telefone")
    @classmethod
    def normalizar_telefone(cls, valor: str) -> str:
        telefone = re.sub(r"\D", "", valor)

        if not 10 <= len(telefone) <= 15:
            raise ValueError("Informe um telefone válido.")

        return telefone

    @field_validator("prompt")
    @classmethod
    def validar_prompt(cls, valor: str) -> str:
        prompt = valor.strip()

        if not prompt:
            raise ValueError("A mensagem não pode ficar vazia.")

        return prompt

    @field_validator("instancia")
    @classmethod
    def validar_instancia(cls, valor: str) -> str:
        instancia = valor.strip().lower()

        if not re.fullmatch(r"[a-z0-9][a-z0-9_-]{0,99}", instancia):
            raise ValueError(
                "A instância deve usar letras minúsculas, números, hífen ou sublinhado."
            )

        return instancia

@router.post("/chat")
async def resposta(
    dados: RequisicaoChat,
    db: Session = Depends(get_db),
):
    cliente = buscar_ou_criar_cliente(
        db=db,
        telefone=dados.telefone,
        instancia=dados.instancia,
    )

    conversa = buscar_ou_criar_conversa(
        db=db,
        cliente=cliente,
    )

    historico = buscar_historico(
        db=db,
        conversa=conversa,
        limite=settings.CHAT_HISTORY_LIMIT,
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

    try:
        resposta_llm = await gerar_resposta(
            prompt=dados.prompt,
            historico=historico_ollama,
        )
    except OllamaIndisponivelError as exc:
        db.rollback()
        logger.exception("Falha ao obter resposta do Ollama.")

        raise HTTPException(
            status_code=503,
            detail="Assistente temporariamente indisponível. Tente novamente em instantes.",
        ) from exc

    criar_mensagem(
        db=db,
        conversa=conversa,
        conteudo=resposta_llm,
        papel=PapelMensagem.ASSISTANT,
    )

    db.commit()

    return {"Texto LLM": resposta_llm}