from app.models import db, SpendingCategory, Spending, Category, environment, SCHEMA
from sqlalchemy.sql import text

def seed_spending_categories():
    """
    Seeds spending categories into the database, linking spendings and categories.
    """
    # Fetch existing spendings and categories
    spendings = Spending.query.all()
    categories = Category.query.all()

    if len(spendings) < 2 or len(categories) < 3:
        raise Exception("Not enough spendings or categories to seed spending categories.")

    # Create spending category data
    spending_categories_data = []

    # Seed spending categories
    for data in spending_categories_data:
        # Ensure the spending and category IDs exist
        spending = Spending.query.get(data["spending_id"])
        category = Category.query.get(data["category_id"])

        if not spending:
            raise Exception(f"Spending ID {data['spending_id']} not found.")
        if not category:
            raise Exception(f"Category ID {data['category_id']} not found.")

        # Create and add the spending category
        spending_category = SpendingCategory(
            spending_id=data["spending_id"],
            category_id=data["category_id"]
        )
        db.session.add(spending_category)

    # Commit changes
    db.session.commit()
    print("Spending categories seeding completed successfully.")


def undo_spending_categories():
    """
    Removes all spending categories from the database and resets primary keys.
    """
    try:
        if environment == "production":
            db.session.execute(f"TRUNCATE TABLE {SCHEMA}.spending_categories RESTART IDENTITY CASCADE;")
        else:
            db.session.execute(text("DELETE FROM spending_categories"))
        db.session.commit()
        print("Spending categories table cleared successfully.")
    except Exception as e:
        print(f"An error occurred while clearing the spending categories table: {e}")
        db.session.rollback()
