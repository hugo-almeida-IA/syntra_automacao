from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_model import BaseModel


if TYPE_CHECKING:
    from app.models.documento import Documento


class Embedding(BaseModel):
    __tablename__ = "embeddings"

    documento_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "documentos.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    chunk_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    ordem: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    texto: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    documento: Mapped["Documento"] = relationship(
        back_populates="embeddings",
    )