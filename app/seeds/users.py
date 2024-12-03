from app.models import db, User, environment, SCHEMA
from sqlalchemy.sql import text

def seed_users():
    """
    Seeds initial users into the database.
    """
    users = [
        User(username='Demo', email='demo@aa.io', password='password'),
        User(username='marnie', email='marnie@aa.io', password='password'),
        User(username='bobbie', email='bobbie@aa.io', password='password'),
    ]

    # Use bulk save for efficient insertion
    db.session.bulk_save_objects(users)
    db.session.commit()


def undo_users():
    """
    Removes all user data from the database and resets primary keys.
    """
    if environment == "production":
        db.session.execute(f"TRUNCATE TABLE {SCHEMA}.users RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM users"))
    db.session.commit()
