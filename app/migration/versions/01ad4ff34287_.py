"""empty message

Revision ID: 01ad4ff34287
Revises: 
Create Date: 2022-07-20 11:29:20.574174

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01ad4ff34287'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reviews',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('publication_date', sa.DateTime(), nullable=True),
    sa.Column('review', sa.Text(), nullable=True),
    sa.Column('rating', sa.Float(), nullable=True),
    sa.Column('username', sa.VARCHAR(), nullable=True),
    sa.Column('bank', sa.VARCHAR(), nullable=True),
    sa.Column('url', sa.VARCHAR(), nullable=True),
    sa.Column('address', sa.VARCHAR(), nullable=True),
    sa.Column('source', sa.VARCHAR(), nullable=True),
    sa.Column('category_name', sa.VARCHAR(), nullable=True),
    sa.Column('category_percent', sa.Float(), nullable=True),
    sa.Column('custom_categories', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reviews')
    # ### end Alembic commands ###
