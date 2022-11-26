"""empty message

Revision ID: 4831dae4f74d
Revises: 
Create Date: 2022-11-22 22:16:51.242069

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4831dae4f74d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('producto',
    sa.Column('id_producto', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=250), nullable=True),
    sa.Column('categoria', sa.String(length=250), nullable=True),
    sa.Column('serie', sa.String(length=250), nullable=True),
    sa.PrimaryKeyConstraint('id_producto')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('registered_on', sa.DateTime(), nullable=False),
    sa.Column('admin', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('user_images',
    sa.Column('id_imagen', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=128), nullable=False),
    sa.Column('data', sa.LargeBinary(), nullable=False),
    sa.Column('rendered_data', sa.Text(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id_imagen')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_images')
    op.drop_table('users')
    op.drop_table('producto')
    # ### end Alembic commands ###
