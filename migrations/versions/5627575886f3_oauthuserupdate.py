"""OAuthUserUpdate

Revision ID: 5627575886f3
Revises: 4b445c0a0983
Create Date: 2020-12-13 00:09:59.372912

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5627575886f3'
down_revision = '4b445c0a0983'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute('UPDATE users SET type = \'bookbnb_user\' WHERE type IS NULL')
    op.alter_column('users', 'type',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'type',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    # ### end Alembic commands ###
