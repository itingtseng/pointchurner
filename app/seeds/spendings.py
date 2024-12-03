from app.models import db, Spending, SpendingCategory, Category


def seed_spending():
    # Create Spending entries for users
    spendings = [
        Spending(user_id=1),
        Spending(user_id=2)
    ]

    db.session.bulk_save_objects(spendings)
    db.session.commit()

    # Retrieve the created spendings
    spending1, spending2 = spendings

    # Associate categories with spending profiles and assign priorities
    spending_categories_data = [
        {'spending_id': spending1.id, 'category_id': 1, 'priority': 1},
        {'spending_id': spending1.id, 'category_id': 2, 'priority': 2},
        {'spending_id': spending2.id, 'category_id': 3, 'priority': 1},
        {'spending_id': spending2.id, 'category_id': 4, 'priority': 2},
    ]

    # Verify that categories exist before creating SpendingCategory entries
    for data in spending_categories_data:
        category = Category.query.get(data['category_id'])
        if not category:
            raise ValueError(f"Category with id {data['category_id']} does not exist.")
        
        spending_category = SpendingCategory(
            spending_id=data['spending_id'],
            category_id=data['category_id'],
            priority=data['priority']
        )
        db.session.add(spending_category)

    db.session.commit()


def undo_spending():
    if db.engine.url.drivername == 'postgresql':
        db.session.execute('TRUNCATE TABLE spending_categories RESTART IDENTITY CASCADE;')
        db.session.execute('TRUNCATE TABLE spendings RESTART IDENTITY CASCADE;')
    else:
        db.session.execute('DELETE FROM spending_categories')
        db.session.execute('DELETE FROM spendings')
    db.session.commit()
