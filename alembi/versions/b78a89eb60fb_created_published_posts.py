"""created_published_posts

Revision ID: b78a89eb60fb
Revises: 5d2f3bc47349
Create Date: 2023-12-20 21:44:17.618111

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text


# revision identifiers, used by Alembic.
revision: str = 'b78a89eb60fb'
down_revision: Union[str, None] = '5d2f3bc47349'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",
                  sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")))
    op.add_column("posts",
                  sa.Column("published", sa.Boolean(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "created_at")
    op.drop_column("posts", "published")
    pass
