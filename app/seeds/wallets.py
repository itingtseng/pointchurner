from app.models import db, environment, SCHEMA, Wallet
from sqlalchemy.sql import text


def seed_wallets():
    wallets_data = [
        {
            'userId': 1,
            'name': 'Personal Wallet',
            'balance': 1000.00
        },
        {
            'userId': 2,
            'name': 'Travel Wallet',
            'balance': 1500.50
        },
        {
            'userId': 3,
            'name': 'Business Wallet',
            'balance': 750.00
        },
        {
            'userId': 4,
            'name': 'Savings Wallet',
            'balance': 2000.00
        },
        {
            'userId': 5,
            'name': 'Vacation Wallet',
            'balance': 300.00
        },
        {
            'userId': 6,
            'name': 'Family Wallet',
            'balance': 1200.75
        },
        {
            'userId': 7,
            'name': 'Shopping Wallet',
            'balance': 500.00
        },
        {
            'userId': 8,
            'name': 'Emergency Wallet',
            'balance': 0.00
        },
        {
            'userId': 9,
            'name': 'Gift Wallet',
            'balance': 250.00
        },
        {
            'userId': 10,
            'name': 'Miscellaneous Wallet',
            'balance': 100.00
        }
    ]

    db.session.bulk_insert_mappings(Wallet, wallets_data)
    db.session.commit()


def undo_wallets():
    if environment == "production":
        db.session.execute(f"TRUNCATE TABLE {SCHEMA}.wallets RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM wallets"))

    db.session.commit()
