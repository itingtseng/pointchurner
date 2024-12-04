from app.models import db, SpendingCategory, Spending, Category


def seed_spending_categories():
    # Fetch existing spendings and categories
    spendings = Spending.query.all()
    categories = Category.query.all()

    if len(spendings) < 2 or len(categories) < 3:
        raise Exception("Not enough spendings or categories to seed spending categories.")

    # Create spending category data
    spending_categories_data = [
        {"spending_id": spendings[0].id, "category_id": categories[0].id},
        {"spending_id": spendings[0].id, "category_id": categories[1].id},
        {"spending_id": spendings[1].id, "category_id": categories[1].id},
        {"spending_id": spendings[1].id, "category_id": categories[2].id},
        {"spending_id": spendings[0].id, "category_id": categories[2].id},
    ]

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


def undo_spending_categories():
    if db.engine.url.drivername == "postgresql":
        db.session.execute("TRUNCATE TABLE spending_categories RESTART IDENTITY CASCADE;")
    else:
        db.session.execute("DELETE FROM spending_categories;")
    db.session.commit()
