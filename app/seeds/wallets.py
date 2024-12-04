from app.models import db, environment, SCHEMA, Wallet
from sqlalchemy.sql import text


def seed_wallets():
    """
    Seeds initial wallets into the database.
    """
    wallets_data = [
        {'user_id': 1},
        {'user_id': 2},
        {'user_id': 3},
        {'user_id': 4},
        {'user_id': 5},
        {'user_id': 6},
        {'user_id': 7},
        {'user_id': 8},
        {'user_id': 9},
        {'user_id': 10},
    ]

    # Use bulk insert for efficient seeding
    db.session.bulk_insert_mappings(Wallet, wallets_data)
    db.session.commit()


def undo_wallets():
    """
    Deletes all wallets and resets the primary key sequence.
    """
    if environment == "production":
        db.session.execute(f"TRUNCATE TABLE {SCHEMA}.wallets RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM wallets"))
    db.session.commit()
