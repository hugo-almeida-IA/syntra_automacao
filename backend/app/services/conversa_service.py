from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.cliente import Cliente
from app.models.conversa import Conversa
from app.core.enums.status_conversa import StatusConversa


def buscar_ou_criar_conversa(
    db: Session,
    cliente: Cliente,
) -> Conversa:
    resultado = db.execute(
        select(Conversa)
        .where(
            Conversa.cliente_id == cliente.id,
            Conversa.status == StatusConversa.ABERTA.value,
        )
        .order_by(Conversa.iniciada_em.desc())
    )

    conversa = resultado.scalars().first()

    if conversa:
        return conversa

    conversa = Conversa(
        cliente_id=cliente.id,
        status=StatusConversa.ABERTA.value,
    )

    db.add(conversa)
    db.flush()

    return conversa