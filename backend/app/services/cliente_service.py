from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.cliente import Cliente


def buscar_ou_criar_cliente(
    db: Session,
    telefone: str,
) -> Cliente:
    resultado = db.execute(
        select(Cliente).where(Cliente.telefone == telefone)
    )

    cliente = resultado.scalar_one_or_none()

    if cliente:
        return cliente

    cliente = Cliente(
        telefone=telefone,
    )

    db.add(cliente)
    db.flush()

    return cliente