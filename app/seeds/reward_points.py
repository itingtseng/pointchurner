from app.models import db, RewardPoint, Card, Category
import requests
from sqlalchemy.exc import SQLAlchemyError


def seed_reward_points():
    """
    Seed the reward_points table with data fetched from an external JSON source.
    """
    try:
        # Check if the reward_points table exists
        if not db.engine.dialect.has_table(db.engine, "reward_points"):
            print("The reward_points table does not exist. Skipping seeding.")
            return

        # Fetch data from the URL
        url = "https://raw.githubusercontent.com/andenacitelli/credit-card-bonuses-api/main/exports/data.json"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an HTTPError for bad responses
        except requests.RequestException as e:
            print(f"Failed to fetch data from {url}. Error: {e}")
            return

        data = response.json()

        # Process and seed reward points
        for card_data in data:
            # Find the card in the database
            card = Card.query.filter_by(name=card_data["name"]).first()
            if not card:
                print(f"Card {card_data['name']} not found in the database. Skipping.")
                continue

            # Track existing reward points for this card
            existing_reward_points = {rp.category_id for rp in card.reward_points}

            # Iterate through rewards
            for reward_data in card_data.get("rewards", []):
                category_name = reward_data.get("category")
                if not category_name:
                    print(f"Reward entry missing 'category' for card {card.name}. Skipping.")
                    continue

                # Ensure category exists or create it
                category = Category.query.filter_by(name=category_name).first()
                if not category:
                    category = Category(name=category_name)
                    db.session.add(category)
                    db.session.commit()

                # Skip if the reward point already exists
                if category.id in existing_reward_points:
                    print(f"Reward point for category '{category_name}' already exists for card '{card.name}'. Skipping.")
                    continue

                # Add new reward point
                reward_point = RewardPoint(
                    card_id=card.id,
                    category_id=category.id,
                    bonus_point=float(reward_data.get("points", 0)),  # Decimal compatibility
                    multiplier_type=reward_data.get("type", "").strip()
                )
                db.session.add(reward_point)

        # Commit all changes to the database
        db.session.commit()
        print("Reward points seeding completed successfully.")

    except SQLAlchemyError as e:
        print(f"Database error during seeding: {e}")
        db.session.rollback()  # Rollback in case of database errors

    except Exception as e:
        print(f"An unexpected error occurred during seeding: {e}")
        db.session.rollback()


def undo_reward_points():
    """
    Remove all entries from the reward_points table and reset its identity.
    """
    try:
        # Check if the reward_points table exists
        if not db.engine.dialect.has_table(db.engine, "reward_points"):
            print("The reward_points table does not exist. Skipping undo.")
            return

        # Remove all entries from the reward_points table
        if db.engine.url.drivername == "postgresql":
            db.session.execute("TRUNCATE TABLE reward_points RESTART IDENTITY CASCADE;")
        else:
            db.session.execute("DELETE FROM reward_points")
        db.session.commit()
        print("Reward points table cleared successfully.")

    except SQLAlchemyError as e:
        print(f"Database error while clearing the reward_points table: {e}")
        db.session.rollback()

    except Exception as e:
        print(f"An unexpected error occurred while clearing the reward_points table: {e}")
        db.session.rollback()
