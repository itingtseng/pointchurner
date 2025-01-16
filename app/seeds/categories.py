from app.models import db, Category, environment, SCHEMA
from sqlalchemy.sql import text

def seed_categories():
    """
    Seeds initial categories and subcategories into the database.
    """
    # Define categories and subcategories
    categories_data = [
        {"id": 1, "name": "dining", "parent_id": None},
        {"id": 2, "name": "restaurants", "parent_id": 1},
        {"id": 3, "name": "fast food", "parent_id": 1},
        {"id": 4, "name": "travel", "parent_id": None},
        {"id": 5, "name": "airlines", "parent_id": 4},
        {"id": 6, "name": "hotels", "parent_id": 4},
        {"id": 7, "name": "car rentals", "parent_id": 4},
        {"id": 8, "name": "groceries", "parent_id": None},
        {"id": 9, "name": "supermarkets", "parent_id": 8},
        {"id": 10, "name": "specialty stores", "parent_id": 8},
        {"id": 11, "name": "transportation", "parent_id": None},
        {"id": 12, "name": "gas stations", "parent_id": 11},
        {"id": 13, "name": "electric charging stations", "parent_id": 11},
        {"id": 14, "name": "rideshare", "parent_id": 11},
        {"id": 15, "name": "taxi", "parent_id": 11},
        {"id": 16, "name": "online shopping", "parent_id": None},
        {"id": 17, "name": "e-commerce", "parent_id": 16},
        {"id": 18, "name": "subscriptions", "parent_id": 16},
        {"id": 19, "name": "utility", "parent_id": None},
        {"id": 20, "name": "cable", "parent_id": 19},
        {"id": 21, "name": "wireless", "parent_id": 19},
        {"id": 22, "name": "phone", "parent_id": 19},
        {"id": 23, "name": "office supplies", "parent_id": None},
        {"id": 24, "name": "shipping", "parent_id": 23},
        {"id": 25, "name": "wholesale", "parent_id": 23},
        {"id": 26, "name": "business", "parent_id": 23},
        {"id": 27, "name": "health & wellness", "parent_id": None},
        {"id": 28, "name": "pharmacy", "parent_id": 27},
        {"id": 29, "name": "medical", "parent_id": 27},
        {"id": 30, "name": "retail", "parent_id": None},
        {"id": 31, "name": "international", "parent_id": None},
        {"id": 32, "name": "flexible", "parent_id": None},
        {"id": 33, "name": "surprise me", "parent_id": None},
        {"id": 34, "name": "high value", "parent_id": None},
        {"id": 35, "name": "entertainment", "parent_id": None},
        {"id": 36, "name": "rent", "parent_id": None},
        {"id": 37, "name": "other", "parent_id": None},
    ]

    # Seed categories
    for category in categories_data:
        existing_category = Category.query.filter_by(name=category["name"], parent_category_id=category["parent_id"]).first()
        if not existing_category:
            new_category = Category(
                id=category["id"],
                name=category["name"],
                parent_category_id=category["parent_id"]
            )
            db.session.add(new_category)

    db.session.commit()


def undo_categories():
    """
    Removes all categories from the database and resets primary keys.
    """
    if environment == "production":
        db.session.execute(f"TRUNCATE TABLE {SCHEMA}.categories RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM categories"))
    db.session.commit()
