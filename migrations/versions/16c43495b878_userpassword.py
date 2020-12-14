"""UserPassword

Revision ID: 16c43495b878
Revises: 5627575886f3
Create Date: 2020-12-14 00:07:13.225766

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '16c43495b878'
down_revision = '5627575886f3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(length=128),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(length=128),
               nullable=False)
    # ### end Alembic commands ###