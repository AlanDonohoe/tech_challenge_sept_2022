"""use time now as default for updated_at

Revision ID: 237fb65bf444
Revises: d7d8db121720
Create Date: 2022-09-27 12:04:48.385014

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "237fb65bf444"
down_revision = "d7d8db121720"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("user", "updated_at", server_default=sa.text("now()"))
    op.alter_column("event", "updated_at", server_default=sa.text("now()"))


def downgrade() -> None:
    op.alter_column("user", "updated_at", server_default=False)
    op.alter_column("event", "updated_at", server_default=False)
