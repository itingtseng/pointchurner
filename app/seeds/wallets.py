from app.models import db, Wallet, environment, SCHEMA
from datetime import datetime
from sqlalchemy.sql import text


def seed_wallets():
    """
    Seeds wallets into the database for multiple users.
    """
    try:
        # Define wallet data
        wallets_data = [
            {"user_id": 1, "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()},
            {"user_id": 2, "created_at": datetime.utcnow(), "updated_at": datetime.utcnow()},
        ]

        # Seed wallets
        for data in wallets_data:
            wallet = Wallet(
                user_id=data["user_id"],
                created_at=data["created_at"],
                updated_at=data["updated_at"],
            )
            db.session.add(wallet)

        # Commit changes
        db.session.commit()
        print("Wallets seeding completed successfully.")
    except Exception as e:
        print(f"An error occurred during wallet seeding: {e}")
        db.session.rollback()


def undo_wallets():
    """
    Removes all wallets from the database and resets primary keys.
    """
    try:
        if environment == "production":
            db.session.execute(f"TRUNCATE TABLE {SCHEMA}.wallets RESTART IDENTITY CASCADE;")
        else:
            db.session.execute(text("DELETE FROM wallets"))
        db.session.commit()
        print("Wallets table cleared successfully.")
    except Exception as e:
        print(f"An error occurred while clearing the wallets table: {e}")
        db.session.rollback()
