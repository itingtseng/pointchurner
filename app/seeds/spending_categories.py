from app.models import db, SpendingCategory, Spending, Category, environment, SCHEMA
from sqlalchemy.sql import text


def seed_spending_categories():
    """
    Seeds spending categories into the database, linking spendings and categories.
    """
    # Fetch existing spendings
    spendings = Spending.query.all()

    if len(spendings) < 2:
        raise Exception("Not enough spendings to seed spending categories.")

    # Fixed spending category data with explicit category IDs
    spending_categories_data = [
        {"spending_id": spendings[0].id, "category_id": 1, "notes": "Initial seed note 1"},
        {"spending_id": spendings[0].id, "category_id": 2, "notes": "Initial seed note 2"},
        {"spending_id": spendings[1].id, "category_id": 3, "notes": None},  # No notes provided
    ]

    # Seed spending categories
    for data in spending_categories_data:
        # Fetch spending and category by ID
        spending = Spending.query.get(data["spending_id"])
        category = Category.query.get(data["category_id"])

        # Validate IDs
        if not spending:
            raise Exception(f"Spending ID {data['spending_id']} not found.")
        if not category:
            raise Exception(f"Category ID {data['category_id']} not found.")

        # Create and add the spending category
        spending_category = SpendingCategory(
            spending_id=spending.id,
            category_id=category.id,
            notes=data["notes"]
        )
        db.session.add(spending_category)

        # Debugging output
        print(f"Seeded spending category: Spending ID {spending.id}, Category ID {category.id}")

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
