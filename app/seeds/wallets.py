from app.models import db, environment, SCHEMA, Wallet
from sqlalchemy.sql import text


def seed_wallets():
    """
    Seeds initial wallets into the database.
    """
    wallets_data = [
        {'user_id': 1, 'name': 'Personal Wallet'},
        {'user_id': 2, 'name': 'Travel Wallet'},
        {'user_id': 3, 'name': 'Business Wallet'},
        {'user_id': 4, 'name': 'Savings Wallet'},
        {'user_id': 5, 'name': 'Vacation Wallet'},
        {'user_id': 6, 'name': 'Family Wallet'},
        {'user_id': 7, 'name': 'Shopping Wallet'},
        {'user_id': 8, 'name': 'Emergency Wallet'},
        {'user_id': 9, 'name': 'Gift Wallet'},
        {'user_id': 10, 'name': 'Miscellaneous Wallet'},
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
