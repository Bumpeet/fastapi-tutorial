"""creating user table

Revision ID: 121d5f54cf5f
Revises: b78a89eb60fb
Create Date: 2023-12-20 22:09:41.845451

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '121d5f54cf5f'
down_revision: Union[str, None] = 'b78a89eb60fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",
                    sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
                    sa.Column("email", sa.String(), nullable=False, unique=True),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_at", sa.DateTime(timezone=True), 
                              nullable=False, server_default=sa.text("now()")))
    op.add_column("posts", 
                  sa.Column("user_id", sa.Integer(), nullable=False))
    
    op.create_foreign_key("post_user_fk", source_table='posts', referent_table="users",
                          local_cols=["user_id"], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_column("posts", "user_id")
    op.drop_table("users")
    pass
