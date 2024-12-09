from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import Wallet, Card, db

wallet_routes = Blueprint('wallets', __name__)

# Get the current user's wallet and associated cards
@wallet_routes.route('/')
@login_required
def get_wallet():
    wallet = Wallet.query.filter_by(userId=current_user.id).first()
    if not wallet:
        return {"message": "Wallet not found!"}, 404

    wallet_details = {
        "id": wallet.id,
        "cards": [
            {
                "id": card.id,
                "name": card.name,
                "nickname": card.nickname,
                "network": card.network,
                "issuer": card.issuer,
                "imageUrl": card.image_url,
                "url": card.url,
            }
            for card in wallet.cards
        ],
    }
    return jsonify(wallet_details)

# Add a card to the user's wallet
@wallet_routes.route('/cards', methods=["POST"])
@login_required
def add_card():
    """
    Add a card to the user's wallet.
    """
    data = request.json
    if not data or not data.get("card_id") or not data.get("nickname") or not data.get("network"):
        return {"message": "Invalid input data"}, 400

    wallet = Wallet.query.filter_by(userId=current_user.id).first()
    if not wallet:
        return {"message": "Wallet not found!"}, 404

    # Check if the card already exists in the wallet
    existing_card = Card.query.filter_by(id=data["card_id"], walletId=wallet.id).first()
    if existing_card:
        return {"message": "Card already exists in wallet!"}, 409

    # Check if the card exists in the database
    card = Card.query.get(data["card_id"])
    if not card:
        return {"message": "Card not found!"}, 404

    # Add the card to the wallet
    card.walletId = wallet.id
    card.nickname = data["nickname"]
    card.network = data["network"]
    db.session.commit()

    return jsonify(card.to_dict()), 201

# Update card details in the wallet
@wallet_routes.route('/cards/<int:cardId>', methods=["PUT"])
@login_required
def update_card(cardId):
    """
    Update card details in the wallet.
    """
    wallet = Wallet.query.filter_by(userId=current_user.id).first()
    if not wallet:
        return {"message": "Wallet not found!"}, 404

    card = Card.query.filter_by(id=cardId, walletId=wallet.id).first()
    if not card:
        return {"message": "Card not found in wallet!"}, 404

    data = request.json
    card.nickname = data.get("nickname", card.nickname)
    card.network = data.get("network", card.network)
    db.session.commit()

    return jsonify(card.to_dict()), 200

# Remove a card from the wallet
@wallet_routes.route('/cards/<int:cardId>', methods=["DELETE"])
@login_required
def remove_card(cardId):
    """
    Remove a card from the wallet.
    """
    wallet = Wallet.query.filter_by(userId=current_user.id).first()
    if not wallet:
        return {"message": "Wallet not found!"}, 404

    card = Card.query.filter_by(id=cardId, walletId=wallet.id).first()
    if not card:
        return {"message": "Card not found in wallet!"}, 404

    # Remove association with the wallet
    card.walletId = None
    db.session.commit()

    return {"message": "Card successfully removed from wallet"}, 200
