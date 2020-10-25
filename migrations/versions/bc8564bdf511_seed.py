"""seed

Revision ID: bc8564bdf511
Revises: 
Create Date: 2020-10-17 15:57:23.678971

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc8564bdf511'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(128), nullable=False),
    sa.Column('password', sa.String(30), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('new_field', sa.Integer(), nullable=False),
    sa.Column('other_new_field', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
