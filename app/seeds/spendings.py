from app.models import db, Spending, environment, SCHEMA
from sqlalchemy.sql import text

def seed_spendings():
    """
    Seeds spendings into the database.
    """
    try:
        # Create spending objects
        spendings = [
            Spending(user_id=1),
            Spending(user_id=2),
        ]
        
        # Add spendings to the session and commit to generate IDs
        for spending in spendings:
            db.session.add(spending)
        db.session.commit()  # Ensure spending_id is generated

        # Verify that the spending IDs are generated
        if not all(spending.id for spending in spendings):
            raise Exception("Failed to generate IDs for spendings.")

        print("Spendings seeding completed successfully.")
    except Exception as e:
        print(f"An error occurred during seeding: {e}")
        db.session.rollback()


def undo_spendings():
    """
    Removes all spendings from the database, resetting primary keys.
    """
    try:
        if environment == "production":
            db.session.execute(f"TRUNCATE TABLE {SCHEMA}.spendings RESTART IDENTITY CASCADE;")
        else:
            db.session.execute(text("DELETE FROM spendings"))
        db.session.commit()
        print("Spendings table cleared successfully.")
    except Exception as e:
        print(f"An error occurred while clearing the spendings table: {e}")
        db.session.rollback()
