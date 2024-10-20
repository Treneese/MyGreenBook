"""Fix backref conflicts for notifications

Revision ID: 82f25e7b59f5
Revises: 1086b92511b4
Create Date: 2024-08-26 20:05:54.879137

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '82f25e7b59f5'
down_revision = '1086b92511b4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notifications', schema=None) as batch_op:
        batch_op.add_column(sa.Column('message', sa.String(length=500), nullable=False))
        batch_op.drop_column('content')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notifications', schema=None) as batch_op:
        batch_op.add_column(sa.Column('content', sa.TEXT(), nullable=False))
        batch_op.drop_column('message')

    # ### end Alembic commands ###
