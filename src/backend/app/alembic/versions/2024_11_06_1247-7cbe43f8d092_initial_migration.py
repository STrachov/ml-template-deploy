"""initial migration

Revision ID: 7cbe43f8d092
Revises: 
Create Date: 2024-11-06 12:47:14.658778

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '7cbe43f8d092'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('user',
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('full_name', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=True),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('hashed_password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_table('action',
    sa.Column('model_name', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('prompt', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('output', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('cost', sa.Float(), nullable=False),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('owner_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )



def downgrade():
    op.drop_table('action')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')

