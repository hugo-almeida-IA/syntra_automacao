from typing import TYPE_CHECKING
from uuid import UUID
from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from app.models.base_model import BaseModel
from app.core.enums.status_conversa import StatusConversa

if TYPE_CHECKING:
    from app.models.cliente import Cliente
    from app.models.mensagem import Mensagem


class Conversa(BaseModel):
    __tablename__ = "conversas"

    cliente_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "clientes.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    titulo: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default=StatusConversa.ABERTA.value,
        nullable=False,
    )

    iniciada_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    encerrada_em: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    cliente: Mapped["Cliente"] = relationship(
        back_populates="conversas"
    )

    mensagens: Mapped[list["Mensagem"]] = relationship(
        back_populates="conversa",
        cascade="all, delete-orphan",
    )