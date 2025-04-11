"""initial migration

Revision ID: 7cbe43f8d092
Revises: 
Create Date: 2024-11-06 12:47:14.658778

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from enum import Enum


# revision identifiers, used by Alembic.
revision = '7cbe43f8d092'
down_revision = None
branch_labels = None
depends_on = None


# Define enum for token types
class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


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
    sa.Column('cost', sa.Float(), nullable=True),
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('owner_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    
    # RefreshToken table
    op.create_table('refreshtoken',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('refresh_token', sqlmodel.sql.sqltypes.AutoString(), nullable=False, unique=True),
    sa.Column('expires_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('revoked', sa.Boolean(), nullable=False, server_default='FALSE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    
    # TokenBlacklist table
    op.create_table('tokenblacklist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('token_type', sa.String(), nullable=False),
    sa.Column('blacklisted_at', sa.DateTime(), nullable=False),
    sa.Column('expires_at', sa.DateTime(), nullable=False),
    sa.Column('blacklisted_by', sa.Uuid(), nullable=True),
    sa.ForeignKeyConstraint(['blacklisted_by'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tokenblacklist_token'), 'tokenblacklist', ['token'], unique=False)
    op.create_index(op.f('ix_tokenblacklist_token_type'), 'tokenblacklist', ['token_type'], unique=False)


def downgrade():
    op.drop_table('tokenblacklist')
    op.drop_table('refreshtoken')
    op.drop_table('action')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')

