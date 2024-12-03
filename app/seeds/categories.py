from app.models import db, Category
from sqlalchemy.sql import text


def seed_categories():
    # Define categories and subcategories
    categories_data = [
        {
            "name": "dining",
            "subcategories": [
                {"name": "restaurants"},
                {"name": "fast food"}
            ]
        },
        {
            "name": "travel",
            "subcategories": [
                {"name": "airlines"},
                {"name": "hotels"},
                {"name": "car rentals"}
            ]
        },
        {
            "name": "groceries",
            "subcategories": [
                {"name": "supermarkets"},
                {"name": "specialty stores"}
            ]
        },
        {
            "name": "gas",
            "subcategories": [
                {"name": "gas stations"},
                {"name": "electric charging stations"}
            ]
        },
        {
            "name": "entertainment",
            "subcategories": [
                {"name": "movies"},
                {"name": "concerts"},
                {"name": "theaters"}
            ]
        },
        {
            "name": "online shopping",
            "subcategories": [
                {"name": "e-commerce"},
                {"name": "subscriptions"}
            ]
        },
    ]

    # Create categories and their subcategories
    for category_data in categories_data:
        category = Category(name=category_data["name"])
        db.session.add(category)
        db.session.commit()

        # Add subcategories
        for subcategory_data in category_data.get("subcategories", []):
            subcategory = Category(name=subcategory_data["name"], parent_category_id=category.id)
            db.session.add(subcategory)

    db.session.commit()


def undo_categories():
    if db.engine.url.drivername == 'postgresql':
        db.session.execute("TRUNCATE TABLE categories RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM categories"))

    db.session.commit()
