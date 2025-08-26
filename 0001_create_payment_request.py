from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'payment_requests',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('hash', sa.String(length=64), nullable=False),
        sa.Column('amount_minor', sa.Integer(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=True),
        sa.Column('stripe_session_id', sa.String(length=128), nullable=True),
    )
    op.create_index('ix_payment_requests_hash', 'payment_requests', ['hash'], unique=True)
    op.create_index('ix_payment_requests_status', 'payment_requests', ['status'])
    op.create_index('ix_payment_requests_stripe_session_id', 'payment_requests', ['stripe_session_id'])

def downgrade() -> None:
    op.drop_index('ix_payment_requests_stripe_session_id', table_name='payment_requests')
    op.drop_index('ix_payment_requests_status', table_name='payment_requests')
    op.drop_index('ix_payment_requests_hash', table_name='payment_requests')
    op.drop_table('payment_requests')
