from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.conversa import Conversa
from app.models.mensagem import Mensagem
from app.core.enums.papel_mensagem import PapelMensagem


def criar_mensagem(
    db: Session,
    conversa: Conversa,
    conteudo: str,
    papel: PapelMensagem,
) -> Mensagem:
    mensagem = Mensagem(
        conversa_id=conversa.id,
        papel=papel.value,
        conteudo=conteudo,
    )

    db.add(mensagem)
    db.flush()

    return mensagem


def buscar_historico(
    db: Session,
    conversa: Conversa,
) -> list[Mensagem]:
    resultado = db.execute(
        select(Mensagem)
        .where(Mensagem.conversa_id == conversa.id)
        .order_by(Mensagem.created_at.asc())
    )

    return list(resultado.scalars().all())