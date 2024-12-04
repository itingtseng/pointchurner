from app.models import db, Card, RewardPoint, Category
import requests

def seed_cards():
    url = "https://raw.githubusercontent.com/andenacitelli/credit-card-bonuses-api/main/exports/data.json"
    response = requests.get(url)
    data = response.json()

    for card_data in data:
        # Safely handle fields
        name = card_data.get("name", "Unknown Card")
        issuer = card_data.get("issuer", "Unknown Issuer")
        url = card_data.get("url", "")
        image_url = card_data.get("image_url", "")

        # Create Card
        card = Card(
            name=name,
            issuer=issuer,
            url=url,
            image_url=image_url
        )
        db.session.add(card)
        db.session.commit()

        # Add Reward Points
        for reward_data in card_data.get("reward_points", []):
            category_name = reward_data.get("category_id", "Unknown Category")
            category = Category.query.filter_by(name=category_name).first()
            if not category:
                category = Category(name=category_name)
                db.session.add(category)
                db.session.commit()

            reward_point = RewardPoint(
                card_id=card.id,
                category_id=category.id,
                bonus_point=reward_data.get("bonus_point", 0.0),
                multiplier_type=reward_data.get("multiplier_type", ""),
            )
            db.session.add(reward_point)

    db.session.commit()

def undo_cards():
    db.session.execute("DELETE FROM reward_points")
    db.session.execute("DELETE FROM cards")
    db.session.commit()
