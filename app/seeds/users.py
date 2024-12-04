from app.models import db, User, environment, SCHEMA
from sqlalchemy.sql import text

def seed_users():
    """
    Seeds initial users into the database with first and last names.
    """
    users = [
        User(username='Demo', email='demo@aa.io', password='password', firstname='Demo', lastname='User'),
        User(username='marnie', email='marnie@aa.io', password='password', firstname='Marnie', lastname='Smith'),
        User(username='bobbie', email='bobbie@aa.io', password='password', firstname='Bobbie', lastname='Brown'),
        User(username='alice', email='alice@aa.io', password='password', firstname='Alice', lastname='Johnson'),
        User(username='charlie', email='charlie@aa.io', password='password', firstname='Charlie', lastname='Williams'),
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
