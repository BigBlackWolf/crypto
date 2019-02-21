"""empty message

Revision ID: b94393e16c5f
Revises: 
Create Date: 2019-02-21 14:55:16.452490

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b94393e16c5f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cookie', sa.Text(), nullable=False),
    sa.Column('expire_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rsa_keys',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('key_size', sa.Integer(), nullable=False),
    sa.Column('module', sa.Text(), nullable=False),
    sa.Column('public_exponent', sa.Text(), nullable=False),
    sa.Column('secret', sa.Text(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('key_size', 'secret', name='unique_secret_key')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('rsa_keys')
    op.drop_table('users')
    # ### end Alembic commands ###