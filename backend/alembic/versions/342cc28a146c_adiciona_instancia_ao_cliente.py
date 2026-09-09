"""adiciona instancia ao cliente

Revision ID: 342cc28a146c
Revises: 8ef537e24f11
Create Date: 2026-09-09 18:39:56.381127

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '342cc28a146c'
down_revision: Union[str, Sequence[str], None] = '8ef537e24f11'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "clientes",
        sa.Column(
            "instancia",
            sa.String(length=100),
            nullable=False,
            server_default=sa.text("'local'"),
        ),
    )
    op.alter_column("clientes", "instancia", server_default=None)

    op.drop_index(op.f("ix_clientes_telefone"), table_name="clientes")
    op.create_unique_constraint(
        "uq_clientes_instancia_telefone",
        "clientes",
        ["instancia", "telefone"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_clientes_instancia_telefone",
        "clientes",
        type_="unique",
    )
    op.create_index(
        op.f("ix_clientes_telefone"),
        "clientes",
        ["telefone"],
        unique=True,
    )
    op.drop_column("clientes", "instancia")