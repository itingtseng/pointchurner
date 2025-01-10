from app.models import db, Wallet, WalletCard, Card, environment, SCHEMA
from datetime import datetime
from sqlalchemy.sql import text

def seed_wallet_cards():
    """
    Seeds wallet cards into the database, linking wallets and cards.
    """
    try:
        # Fetch wallets and specific cards for seeding
        wallets = Wallet.query.all()  # Assuming wallets already exist
        card_19 = Card.query.get(19)  # Get card with ID 19
        card_85 = Card.query.get(85)  # Get card with ID 85

        if len(wallets) < 1 or not card_19 or not card_85:
            raise Exception("Not enough wallets or specific cards to seed wallet cards.")

        # Create wallet card data
        wallet_cards_data = [
            {
                "wallet_id": wallets[0].id,  # Assuming at least one wallet exists
                "card_id": card_19.id,
                "nickname": "My Primary Card",
                "network": "Visa",
            },
            {
                "wallet_id": wallets[0].id,
                "card_id": card_85.id,
                "nickname": "Travel Rewards",
                "network": "MasterCard",
            },
        ]

        # Seed wallet cards
        for data in wallet_cards_data:
            wallet_card = WalletCard(
                wallet_id=data["wallet_id"],
                card_id=data["card_id"],
                nickname=data["nickname"],
                network=data["network"],
                created_at=datetime.utcnow(),
            )
            db.session.add(wallet_card)

        # Commit changes
        db.session.commit()
        print("Wallet cards seeding completed successfully.")
    except Exception as e:
        print(f"An error occurred during wallet card seeding: {e}")
        db.session.rollback()


def undo_wallet_cards():
    """
    Removes all wallet cards from the database and resets primary keys.
    """
    try:
        if environment == "production":
            db.session.execute(f"TRUNCATE TABLE {SCHEMA}.wallet_cards RESTART IDENTITY CASCADE;")
        else:
            db.session.execute(text("DELETE FROM wallet_cards"))
        db.session.commit()
        print("Wallet cards table cleared successfully.")
    except Exception as e:
        print(f"An error occurred while clearing the wallet cards table: {e}")
        db.session.rollback()
