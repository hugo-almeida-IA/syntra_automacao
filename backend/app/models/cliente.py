from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base_model import BaseModel


class Cliente(BaseModel):
    __tablename__ = "clientes"

    nome: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True
    )

    telefone: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
        index=True
    )

    ativo: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )