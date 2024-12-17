from flask import Blueprint, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models import Card, Wallet, RewardPoint, Category, db
from app.forms import AddCardToWalletForm, EditCardForm

card_routes = Blueprint('cards', __name__)

# Get all cards
@card_routes.route('/')
def all_cards():
    """
    Retrieve all cards, optionally filtered by issuer and card type.
    """
    issuer = request.args.get('issuer')
    card_type = request.args.get('card_type')  # "business" or "personal"

    query = Card.query
    if issuer:
        query = query.filter(Card.issuer == issuer)
    if card_type:
        is_business = card_type == "business"
        query = query.filter(Card.is_business == is_business)

    cards = query.all()
    return jsonify({
        "cards": [
            {
                "id": card.id,
                "name": card.name,
                "issuer": card.issuer,
                "image_url": card.image_url,
                "url": card.url,
                "is_business": card.is_business
            }
            for card in cards
        ]
    })


# Get card details by ID
@card_routes.route('/<int:cardId>')
def get_card(cardId):
    """
    Retrieve a single card's details by its ID.
    """
    card = Card.query.get(cardId)
    if not card:
        return {"message": "Card not found!"}, 404

    card_details = {
        "id": card.id,
        "name": card.name,
        "issuer": card.issuer.replace("_", " "),  # Remove underscores from issuer
        "image_url": card.image_url,
        "url": card.url,
        "is_business": card.is_business,
        "reward_points": [
            {
                "category_name": reward.category.name,
                "bonus_point": reward.bonus_point,
                "multiplier_type": reward.multiplier_type,
                "notes": reward.notes
            }
            for reward in card.reward_points
        ]
    }
    return jsonify(card_details)


# Add card to wallet via API
@card_routes.route('/wallet/cards', methods=['POST'])
@login_required
def add_card_to_wallet():
    """
    Add a card to the user's wallet.
    """
    data = request.json
    wallet_id = data.get("wallet_id")
    card_id = data.get("card_id")
    nickname = data.get("nickname")
    network = data.get("network")

    if not wallet_id or not card_id or not nickname or not network:
        return {"message": "All fields are required."}, 400

    # Check if card already exists in the wallet
    existing_card = Wallet.query.filter_by(wallet_id=wallet_id).join(Card).filter(Card.id == card_id).first()
    if existing_card:
        return {"message": "Card already exists in the wallet."}, 409

    # Add the card to the wallet
    new_wallet_card = Wallet(card_id=card_id, wallet_id=wallet_id, nickname=nickname, network=network)
    db.session.add(new_wallet_card)
    db.session.commit()

    return {"message": "Card successfully added to the wallet."}, 201


    
