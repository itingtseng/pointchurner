from app.models import db, Card, RewardPoint, Category
import requests

def seed_cards():
    # Fetch data from the URL
    url = "https://raw.githubusercontent.com/andenacitelli/credit-card-bonuses-api/main/exports/data.json"
    response = requests.get(url)
    data = response.json()

    # Process and seed cards and reward points
    for card_data in data.get("cards", []):
        # Create Card
        card = Card(
            name=card_data["name"],
            issuer=card_data["issuer"],
            network=card_data["network"],
            url=card_data["url"],
            image_url=card_data["image_url"],
        )
        db.session.add(card)
        db.session.commit()

        # Create Reward Points
        for reward_data in card_data.get("reward_points", []):
            # Find or create category
            category = Category.query.filter_by(name=reward_data["category_id"]).first()
            if not category:
                category = Category(name=reward_data["category_id"])
                db.session.add(category)
                db.session.commit()

            # Add reward point
            reward_point = RewardPoint(
                card_id=card.id,
                category_id=category.id,
                bonus_point=reward_data["bonus_point"],
                multiplier_type=reward_data["multiplier_type"],
            )
            db.session.add(reward_point)

    db.session.commit()

def undo_cards():
    db.session.execute("DELETE FROM reward_points")
    db.session.execute("DELETE FROM cards")
    db.session.commit()
