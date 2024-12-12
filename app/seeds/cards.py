from app.models import db, Card, RewardPoint, Category, environment, SCHEMA
from sqlalchemy.sql import text
import requests


def seed_cards():
    """
    Seeds initial cards into the database, including associated reward points and categories.
    Updates the image_url field for each card using local images.
    """
    # Fetch card data from the remote JSON
    url = "https://raw.githubusercontent.com/andenacitelli/credit-card-bonuses-api/main/exports/data.json"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from {url}. Status code: {response.status_code}")

    data = response.json()

    for idx, card_data in enumerate(data, start=1):
        # Safely handle fields
        name = card_data.get("name", "Unknown Card")
        issuer = card_data.get("issuer", "Unknown Issuer")
        card_url = card_data.get("url", "")

        # Use local images based on the card ID
        image_url = f"/seed-images/{idx}.png"

        # Create Card
        card = Card(
            name=name,
            issuer=issuer,
            url=card_url,
            image_url=image_url
        )
        db.session.add(card)
        db.session.commit()

        # Add Reward Points
        for reward_data in card_data.get("rewards", []):
            category_name = reward_data.get("category", "Unknown Category")
            category = Category.query.filter_by(name=category_name).first()
            if not category:
                category = Category(name=category_name)
                db.session.add(category)
                db.session.commit()

            reward_point = RewardPoint(
                card_id=card.id,
                category_id=category.id,
                bonus_point=float(reward_data.get("points", 0.0)),  # Ensure numeric type
                multiplier_type=reward_data.get("type", "").strip(),
            )
            db.session.add(reward_point)

    db.session.commit()


def undo_cards():
    """
    Removes all card data from the database and resets primary keys.
    """
    if environment == "production":
        db.session.execute(f"TRUNCATE TABLE {SCHEMA}.reward_points RESTART IDENTITY CASCADE;")
        db.session.execute(f"TRUNCATE TABLE {SCHEMA}.cards RESTART IDENTITY CASCADE;")
        db.session.execute(f"TRUNCATE TABLE {SCHEMA}.categories RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM reward_points"))
        db.session.execute(text("DELETE FROM cards"))
        db.session.execute(text("DELETE FROM categories"))
    db.session.commit()