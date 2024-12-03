from app.models import db, Spending, SpendingCategory

def seed_spending():
    spending1 = Spending(user_id=1)
    spending2 = Spending(user_id=2)

    db.session.add(spending1)
    db.session.add(spending2)
    db.session.commit()

    # Associate categories with spending profiles and assign priorities
    spending_categories_data = [
        {'spending_id': spending1.id, 'category_id': 1, 'priority': 1},
        {'spending_id': spending1.id, 'category_id': 2, 'priority': 2},
        {'spending_id': spending2.id, 'category_id': 3, 'priority': 1},
        {'spending_id': spending2.id, 'category_id': 4, 'priority': 2},
    ]

    for data in spending_categories_data:
        spending_category = SpendingCategory(**data)
        db.session.add(spending_category)

    db.session.commit()


def undo_spending():
    db.session.execute('TRUNCATE TABLE spending_categories RESTART IDENTITY CASCADE;')
    db.session.execute('TRUNCATE TABLE spendings RESTART IDENTITY CASCADE;')
    db.session.commit()
