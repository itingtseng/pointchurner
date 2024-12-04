from app.models import db, Spending, SpendingCategory, Category

def seed_spendings():
    # Create spending objects and commit them to the database
    spendings = [
        Spending(user_id=1),
        Spending(user_id=2),
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
        {"spending_id": spendings[0].id, "category_id": 1, "priority": 1},
        {"spending_id": spendings[1].id, "category_id": 1, "priority": 1},
    ]

    for sc in spending_categories:
        # Ensure the category exists
        category = Category.query.get(sc["category_id"])
        if not category:
            raise Exception(f"Category ID {sc['category_id']} not found.")
        
        # Create and add the spending category
        spending_category = SpendingCategory(
            spending_id=sc["spending_id"],
            category_id=sc["category_id"],
            priority=sc["priority"]
        )
        db.session.add(spending_category)
    
    # Commit spending categories
    db.session.commit()


def undo_spendings():
    # Undo spendings and associated categories
    if db.engine.url.drivername == 'postgresql':
        db.session.execute("TRUNCATE TABLE spendings, spending_categories RESTART IDENTITY CASCADE;")
    else:
        db.session.execute("DELETE FROM spending_categories;")
        db.session.execute("DELETE FROM spendings;")
    db.session.commit()
