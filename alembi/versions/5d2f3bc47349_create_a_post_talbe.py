"""create a post talbe

Revision ID: 5d2f3bc47349
Revises: 
Create Date: 2023-12-20 20:15:44.687074

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5d2f3bc47349'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts", 
                    sa.Column("id", sa.Integer(), primary_key=True,nullable=False),
                    sa.Column("title", sa.String(), nullable=False),
                    sa.Column("description", sa.String(), nullable=False))

def downgrade() -> None:
    op.drop_table("posts")

