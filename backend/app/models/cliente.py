
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, String, UniqueConstraint

from app.models.base_model import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.conversa import Conversa


class Cliente(BaseModel):
    __tablename__ = "clientes"

    __table_args__ = (
        UniqueConstraint(
            "instancia",
            "telefone",
            name="uq_clientes_instancia_telefone",
        ),
    )

    instancia: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    nome: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True
    )

    telefone: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    ativo: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    conversas: Mapped[list["Conversa"]] = relationship(
        back_populates="cliente",
        cascade="all, delete-orphan"
    )