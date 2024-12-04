from flask.cli import AppGroup
from .users import seed_users, undo_users
from .cards import seed_cards, undo_cards
from .wallets import seed_wallets, undo_wallets
from .categories import seed_categories, undo_categories
from .spendings import seed_spendings, undo_spendings  # Corrected function names
from .reward_points import seed_reward_points, undo_reward_points

from app.models.db import db, environment, SCHEMA

# Creates a seed group to hold our commands
seed_commands = AppGroup('seed')


# Creates the `flask seed all` command
@seed_commands.command('all')
def seed():
    if environment == 'production':
        # Undo all data first in production
        undo_users()
        undo_cards()
        undo_wallets()
        undo_categories()
        undo_spendings()
        undo_reward_points()

    # Seed all data
    seed_users()
    seed_categories()
    seed_cards()
    seed_wallets()
    seed_reward_points()
    seed_spendings()


# Creates the `flask seed undo` command
@seed_commands.command('undo')
def undo():
    undo_reward_points()
    undo_users()
    undo_cards()
    undo_wallets()
    undo_categories()
    undo_spendings()
