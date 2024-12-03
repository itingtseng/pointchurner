from app.models import db, Card, RewardPoint, Category
import requests

def seed_cards():
    url = "https://raw.githubusercontent.com/andenacitelli/credit-card-bonuses-api/main/exports/data.json"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch data from {url}.")
        return

    data = response.json()

    for card_data in data.get("cards", []):
        try:
            card = Card(
                name=card_data["name"],
                issuer=card_data["issuer"],
                network=card_data["network"],
                url=card_data["url"],
                image_url=card_data["image_url"],
            )
            db.session.add(card)

            for reward_data in card_data.get("reward_points", []):
                normalized_name = reward_data["category_id"].strip().lower()
                category = Category.query.filter_by(name=normalized_name).first()
                if not category:
                    category = Category(name=normalized_name)
                    db.session.add(category)

                reward_point = RewardPoint(
                    card=card,
                    category=category,
                    bonus_point=reward_data["bonus_point"],
                    multiplier_type=reward_data["multiplier_type"],
                )
                db.session.add(reward_point)

        except KeyError as e:
            print(f"Skipping card due to missing key: {e}")

    db.session.commit()

def undo_cards():
    db.session.execute("TRUNCATE TABLE reward_points RESTART IDENTITY CASCADE")
    db.session.execute("TRUNCATE TABLE cards RESTART IDENTITY CASCADE")
    db.session.commit()
