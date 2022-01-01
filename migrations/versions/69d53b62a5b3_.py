"""empty message

Revision ID: 69d53b62a5b3
Revises: 14acf7ca49ab
Create Date: 2021-12-10 20:06:36.032650

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69d53b62a5b3'
down_revision = '14acf7ca49ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('picture_wopai', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'picture_wopai')
    # ### end Alembic commands ###
