from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel
from app.core.enums.papel_mensagem import PapelMensagem

if TYPE_CHECKING:
    from app.models.conversa import Conversa


class Mensagem(BaseModel):
    __tablename__ = "mensagens"

    conversa_id: Mapped[UUID] = mapped_column(
        ForeignKey("conversas.id"),
        nullable=False,
        index=True,
    )

    papel: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=PapelMensagem.USER.value,
    )

    conteudo: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    conversa: Mapped["Conversa"] = relationship(
        back_populates="mensagens"
    )