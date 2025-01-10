from app.models import db, Spending, SpendingCategory, Category, environment, SCHEMA
from sqlalchemy.sql import text

def seed_spendings():
    """
    Seeds spendings and their associated categories into the database.
    """
    try:
        # Create spending objects and commit them to the database
        spendings = [
            Spending(user_id=1),
            Spending(user_id=1),
        ]
        
        # Add spendings to the session and commit to generate IDs
        for spending in spendings:
            db.session.add(spending)
        db.session.commit()  # Ensure `spending_id` is generated

        # Verify that the spending IDs are generated
        if not all(spending.id for spending in spendings):
            raise Exception("Failed to generate IDs for spendings.")

        # Create spending categories
        spending_categories = [
            {"spending_id": spendings[0].id, "category_id": 2},
            {"spending_id": spendings[1].id, "category_id": 4},
        ]

        for sc in spending_categories:
            # Ensure the category exists
            category = Category.query.get(sc["category_id"])
            if not category:
                raise Exception(f"Category ID {sc['category_id']} not found.")
            
            # Create and add the spending category
            spending_category = SpendingCategory(
                spending_id=sc["spending_id"],
                category_id=sc["category_id"]
            )
            db.session.add(spending_category)
        
        # Commit spending categories
        db.session.commit()
        print("Spendings and spending categories seeding completed successfully.")
    except Exception as e:
        print(f"An error occurred during seeding: {e}")
        db.session.rollback()


def undo_spendings():
    """
    Removes all spendings and their associated categories from the database, resetting primary keys.
    """
    try:
        if environment == "production":
            db.session.execute(f"TRUNCATE TABLE {SCHEMA}.spending_categories, {SCHEMA}.spendings RESTART IDENTITY CASCADE;")
        else:
            db.session.execute(text("DELETE FROM spending_categories"))
            db.session.execute(text("DELETE FROM spendings"))
        db.session.commit()
        print("Spendings and spending categories tables cleared successfully.")
    except Exception as e:
        print(f"An error occurred while clearing the spending tables: {e}")
        db.session.rollback()
