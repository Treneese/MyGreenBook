"""Add likes column to Review model

Revision ID: db4745c436eb
Revises: b6f4a2471bc7
Create Date: 2024-07-10 09:32:41.886786

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db4745c436eb'
down_revision = 'b6f4a2471bc7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('review_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['review_id'], ['reviews.id'], name=op.f('fk_comments_review_id_reviews')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_comments_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('_alembic_tmp_reviews')
    with op.batch_alter_table('reviews', schema=None) as batch_op:
        batch_op.add_column(sa.Column('likes', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reviews', schema=None) as batch_op:
        batch_op.drop_column('likes')

    op.create_table('_alembic_tmp_reviews',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('content', sa.TEXT(), nullable=False),
    sa.Column('rating', sa.FLOAT(), nullable=False),
    sa.Column('place_id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('created_at', sa.DATETIME(), nullable=False),
    sa.Column('user_username', sa.VARCHAR(length=80), nullable=False),
    sa.Column('user_image', sa.VARCHAR(length=500), nullable=False),
    sa.ForeignKeyConstraint(['place_id'], ['places.id'], name='fk_reviews_place_id_places'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_reviews_user_id_users'),
    sa.ForeignKeyConstraint(['user_image'], ['users.image'], name='fk_reviews_user_image_users'),
    sa.ForeignKeyConstraint(['user_username'], ['users.username'], name='fk_reviews_user_username_users'),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('comments')
    # ### end Alembic commands ###
