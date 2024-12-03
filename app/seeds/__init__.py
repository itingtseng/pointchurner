from flask.cli import AppGroup
from .users import seed_users, undo_users
from .cards import seed_cards, undo_cards
from .wallets import seed_wallets, undo_wallets
from .categories import seed_categories, undo_categories
from .spendings import seed_spending, undo_spending
from .reward_points import seed_reward_points, undo_reward_points  # Add reward points seed

from app.models.db import db, environment, SCHEMA

# Creates a seed group to hold our commands
# So we can type `flask seed --help`
seed_commands = AppGroup('seed')


# Creates the `flask seed all` command
@seed_commands.command('all')
def seed():
    if environment == 'production':
        # Before seeding in production, you want to run the seed undo
        # command, which will truncate all tables prefixed with
        # the schema name (see comment in users.py undo_users function).
        # Make sure to add all your other model's undo functions below
        undo_users()
        undo_cards()
        undo_wallets()
        undo_categories()
        undo_spending()
        undo_reward_points()  # Ensure reward points are undone first in production

    # Seed all data
    seed_users()
    seed_categories()  # Seed categories first to ensure they exist for reward points
    seed_cards()
    seed_wallets()
    seed_reward_points()  # Seed reward points after categories and cards
    seed_spending()


# Creates the `flask seed undo` command
@seed_commands.command('undo')
def undo():
    undo_reward_points()  # Undo reward points first as they depend on categories and cards
    undo_users()
    undo_cards()
    undo_wallets()
    undo_categories()
    undo_spending()
