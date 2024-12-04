from app.models import db, Wallet, WalletCard, Card
from datetime import datetime


def seed_wallet_cards():
    # Fetch wallets and cards for seeding
    wallets = Wallet.query.all()  # Assuming wallets already exist
    cards = Card.query.all()  # Assuming cards already exist

    if len(wallets) < 2 or len(cards) < 5:
        raise Exception("Not enough wallets or cards to seed wallet cards.")

    # Create wallet card data
    wallet_cards_data = [
        {
            "wallet_id": wallets[0].id,
            "card_id": cards[0].id,
            "nickname": "My Primary Card",
            "network": "Visa",
        },
        {
            "wallet_id": wallets[0].id,
            "card_id": cards[1].id,
            "nickname": "Travel Rewards",
            "network": "MasterCard",
        },
        {
            "wallet_id": wallets[1].id,
            "card_id": cards[2].id,
            "nickname": "Cashback",
            "network": "Discover",
        },
        {
            "wallet_id": wallets[1].id,
            "card_id": cards[3].id,
            "nickname": "Groceries Card",
            "network": "Amex",
        },
        {
            "wallet_id": wallets[1].id,
            "card_id": cards[4].id,
            "nickname": None,
            "network": "Visa",
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


def undo_wallet_cards():
    if db.engine.url.drivername == "postgresql":
        db.session.execute("TRUNCATE TABLE wallet_cards RESTART IDENTITY CASCADE;")
    else:
        db.session.execute("DELETE FROM wallet_cards;")
    db.session.commit()
