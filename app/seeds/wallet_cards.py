from app.models import db, Wallet, WalletCard, Card, environment, SCHEMA
from datetime import datetime
from sqlalchemy.sql import text

def seed_wallet_cards():
    """
    Seeds wallet cards into the database, linking wallets and cards.
    """
    try:
        # Fetch wallets and cards for seeding
        wallets = Wallet.query.all()  # Assuming wallets already exist
        cards = Card.query.all()  # Assuming cards already exist

        if len(wallets) < 2 or len(cards) < 5:
            raise Exception("Not enough wallets or cards to seed wallet cards.")

        # Create wallet card data
        wallet_cards_data = [
            {
                "wallet_id": wallets[0].id,
                "card_id": cards[18].id,
                "nickname": "My Primary Card",
                "network": "Visa",
            },
            {
                "wallet_id": wallets[0].id,
                "card_id": cards[84].id,
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
