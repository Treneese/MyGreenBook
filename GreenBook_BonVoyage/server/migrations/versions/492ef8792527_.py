"""empty message

Revision ID: 492ef8792527
Revises: 
Create Date: 2024-07-01 13:46:25.074603

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '492ef8792527'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('places',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('city', sa.String(length=100), nullable=False),
    sa.Column('address', sa.String(length=200), nullable=False),
    sa.Column('safety_rating', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('_password_hash', sa.String(length=128), nullable=False),
    sa.Column('bio', sa.String(length=500), nullable=True),
    sa.Column('image', sa.String(length=500), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('reviews',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('rating', sa.Float(), nullable=False),
    sa.Column('place_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['place_id'], ['places.id'], name=op.f('fk_reviews_place_id_places')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_reviews_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('routes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_routes_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('safetymarks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('is_safe', sa.Boolean(), nullable=False),
    sa.Column('place_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['place_id'], ['places.id'], name=op.f('fk_safetymarks_place_id_places')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_safetymarks_user_id_users')),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('route_place_association',
    sa.Column('route_id', sa.Integer(), nullable=False),
    sa.Column('place_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['place_id'], ['places.id'], name=op.f('fk_route_place_association_place_id_places')),
    sa.ForeignKeyConstraint(['route_id'], ['routes.id'], name=op.f('fk_route_place_association_route_id_routes')),
    sa.PrimaryKeyConstraint('route_id', 'place_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('route_place_association')
    op.drop_table('safetymarks')
    op.drop_table('routes')
    op.drop_table('reviews')
    op.drop_table('users')
    op.drop_table('places')
    # ### end Alembic commands ###