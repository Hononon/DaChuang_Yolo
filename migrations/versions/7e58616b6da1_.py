"""empty message

Revision ID: 7e58616b6da1
Revises: 69d53b62a5b3
Create Date: 2021-12-10 20:08:42.904309

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e58616b6da1'
down_revision = '69d53b62a5b3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('picture_jiqiu', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'picture_jiqiu')
    # ### end Alembic commands ###
