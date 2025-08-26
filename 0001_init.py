from alembic import op
import sqlalchemy as sa

revision = '0001_init'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'requests',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('hash_id', sa.String, unique=True, nullable=False),
        sa.Column('amount', sa.Integer, nullable=False),
        sa.Column('status', sa.String, nullable=False, default='pending'),
    )

def downgrade():
    op.drop_table('requests')
