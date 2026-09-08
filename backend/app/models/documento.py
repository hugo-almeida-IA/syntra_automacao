from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums.status_documento import StatusDocumento
from app.models.base_model import BaseModel


if TYPE_CHECKING:
    from app.models.embedding import Embedding


class Documento(BaseModel):
    __tablename__ = "documentos"

    nome_original: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    nome_armazenado: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    tipo: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    caminho: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    tamanho: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default=StatusDocumento.PROCESSANDO.value,
        nullable=False,
    )

    embeddings: Mapped[list["Embedding"]] = relationship(
        back_populates="documento",
        cascade="all, delete-orphan",
    )