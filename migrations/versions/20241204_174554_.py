"""Add network to wallet_cards, firstname and lastname to users, and adjust reward_points bonus_point

Revision ID: 51881d7c48cb
Revises: acd7cf4b29ce
Create Date: 2024-12-04 17:45:54.389125

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision = '51881d7c48cb'
down_revision = 'acd7cf4b29ce'
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()
    inspector = inspect(connection)

    # Adjust the 'cards' table
    with op.batch_alter_table('cards', schema=None) as batch_op:
        batch_op.alter_column('image_url',
                              existing_type=sa.VARCHAR(length=255),
                              nullable=True)
        batch_op.alter_column('url',
                              existing_type=sa.VARCHAR(length=255),
                              nullable=True)

    # Adjust the 'reward_points' table
    with op.batch_alter_table('reward_points', schema=None) as batch_op:
        batch_op.alter_column('bonus_point',
                              existing_type=sa.FLOAT(),
                              type_=sa.Numeric(precision=10, scale=2),
                              existing_nullable=False)

    # Adjust the 'spendings' table
    spendings_constraints = [fk['name'] for fk in inspector.get_foreign_keys('spendings')]
    with op.batch_alter_table('spendings', schema=None) as batch_op:
        if 'fk_spendings_user_id' in spendings_constraints:
            batch_op.drop_constraint('fk_spendings_user_id', type_='foreignkey')
        batch_op.create_foreign_key('fk_spendings_user_id', 'users', ['user_id'], ['id'], ondelete='CASCADE')

    # Add firstname and lastname to 'users' table
    users_columns = [col['name'] for col in inspector.get_columns('users')]
    with op.batch_alter_table('users', schema=None) as batch_op:
        if 'firstname' not in users_columns:
            batch_op.add_column(sa.Column('firstname', sa.String(length=255), nullable=True))
        if 'lastname' not in users_columns:
            batch_op.add_column(sa.Column('lastname', sa.String(length=255), nullable=True))

    # Add network to 'wallet_cards' table
    wallet_cards_constraints = [fk['name'] for fk in inspector.get_foreign_keys('wallet_cards')]
    with op.batch_alter_table('wallet_cards', schema=None) as batch_op:
        if 'network' not in [col['name'] for col in inspector.get_columns('wallet_cards')]:
            batch_op.add_column(sa.Column('network', sa.String(length=255), nullable=True))
        if 'fk_wallet_cards_wallet_id' in wallet_cards_constraints:
            batch_op.drop_constraint('fk_wallet_cards_wallet_id', type_='foreignkey')
        if 'fk_wallet_cards_card_id' in wallet_cards_constraints:
            batch_op.drop_constraint('fk_wallet_cards_card_id', type_='foreignkey')
        batch_op.create_foreign_key('fk_wallet_cards_wallet_id', 'wallets', ['wallet_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key('fk_wallet_cards_card_id', 'cards', ['card_id'], ['id'], ondelete='CASCADE')


def downgrade():
    connection = op.get_bind()
    inspector = inspect(connection)

    # Reverse changes to 'wallet_cards' table
    wallet_cards_constraints = [fk['name'] for fk in inspector.get_foreign_keys('wallet_cards')]
    with op.batch_alter_table('wallet_cards', schema=None) as batch_op:
        if 'fk_wallet_cards_card_id' in wallet_cards_constraints:
            batch_op.drop_constraint('fk_wallet_cards_card_id', type_='foreignkey')
        if 'fk_wallet_cards_wallet_id' in wallet_cards_constraints:
            batch_op.drop_constraint('fk_wallet_cards_wallet_id', type_='foreignkey')
        batch_op.create_foreign_key('fk_wallet_cards_wallet_id', 'wallets', ['wallet_id'], ['id'])
        batch_op.create_foreign_key('fk_wallet_cards_card_id', 'cards', ['card_id'], ['id'])
        if 'network' in [col['name'] for col in inspector.get_columns('wallet_cards')]:
            batch_op.drop_column('network')

    # Reverse changes to 'users' table
    users_columns = [col['name'] for col in inspector.get_columns('users')]
    with op.batch_alter_table('users', schema=None) as batch_op:
        if 'lastname' in users_columns:
            batch_op.drop_column('lastname')
        if 'firstname' in users_columns:
            batch_op.drop_column('firstname')

    # Reverse changes to 'spendings' table
    spendings_constraints = [fk['name'] for fk in inspector.get_foreign_keys('spendings')]
    with op.batch_alter_table('spendings', schema=None) as batch_op:
        if 'fk_spendings_user_id' in spendings_constraints:
            batch_op.drop_constraint('fk_spendings_user_id', type_='foreignkey')
        batch_op.create_foreign_key('fk_spendings_user_id', 'users', ['user_id'], ['id'])

    # Reverse changes to 'reward_points' table
    with op.batch_alter_table('reward_points', schema=None) as batch_op:
        batch_op.alter_column('bonus_point',
                              existing_type=sa.Numeric(precision=10, scale=2),
                              type_=sa.FLOAT(),
                              existing_nullable=False)

    # Reverse changes to 'cards' table
    with op.batch_alter_table('cards', schema=None) as batch_op:
        batch_op.alter_column('url',
                              existing_type=sa.VARCHAR(length=255),
                              nullable=False)
        batch_op.alter_column('image_url',
                              existing_type=sa.VARCHAR(length=255),
                              nullable=False)
