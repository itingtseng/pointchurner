from flask.cli import AppGroup
from .users import seed_users, undo_users
from .cards import seed_cards, undo_cards
from .wallets import seed_wallets, undo_wallets
from .categories import seed_categories, undo_categories
from .spendings import seed_spendings, undo_spendings
from .reward_points import seed_reward_points, undo_reward_points
from .spending_categories import seed_spending_categories, undo_spending_categories
from .wallet_cards import seed_wallet_cards, undo_wallet_cards
from .images import update_card_images  # Import the image seeder

from app.models.db import db, environment, SCHEMA

# Creates a seed group to hold our commands
seed_commands = AppGroup('seed')


# Creates the `flask seed all` command
@seed_commands.command('all')
def seed():
    if environment == 'production':
        # Undo all data first in production
        undo_wallet_cards()
        undo_spending_categories()
        undo_reward_points()
        undo_spendings()
        undo_categories()
        undo_wallets()
        undo_cards()
        undo_users()

    # Seed all data in the correct order
    seed_users()
    seed_categories()
    seed_cards()
    update_card_images()  # Update image URLs after seeding cards
    seed_wallets()
    seed_spendings()
    seed_reward_points()
    seed_spending_categories()
    seed_wallet_cards()


# Creates the `flask seed undo` command
@seed_commands.command('undo')
def undo():
    undo_wallet_cards()           # Wallet cards depend on wallets
    undo_spending_categories()    # Spending categories depend on categories and spendings
    undo_reward_points()
    undo_spendings()
    undo_categories()
    undo_wallets()
    undo_cards()
    undo_users()
