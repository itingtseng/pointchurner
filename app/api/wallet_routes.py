from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import Wallet, WalletCard, Card, db

wallet_routes = Blueprint('wallets', __name__)

# Get current user's wallet profile
@wallet_routes.route('/session', methods=["GET"])
@login_required
def get_current_user_wallet():
    print(f"Fetching wallet for user ID: {current_user.id}")  # Debugging log
    wallet = Wallet.query.filter_by(user_id=current_user.id).first()
    if not wallet:
        print("Wallet not found.")  # Debugging log
        return {"message": "Wallet not found!"}, 404

    wallet_details = {
    "id": wallet.id,
    "cards": [
        {
            "id": card.id,
            "name": card.name,
            "nickname": wallet_card.nickname,
            "network": wallet_card.network.replace("_", " "),
            "issuer": card.issuer.replace("_", " "),  # Remove underscores
            "image_url": card.image_url,
            "url": card.url,
        }
        for wallet_card in wallet.wallet_cards
        for card in [wallet_card.card]
    ],
}
    print(f"Wallet details: {wallet_details}")  # Debugging log
    return jsonify(wallet_details), 200

# Get details of a specific card in a wallet
@wallet_routes.route('/<int:wallet_id>/cards/<int:card_id>', methods=["GET"])
@login_required
def get_card_in_wallet(wallet_id, card_id):
    """
    Get details of a specific card in a wallet by wallet ID and card ID.
    """
    wallet = Wallet.query.get(wallet_id)
    if not wallet:
        return {"message": "Wallet not found!"}, 404

    # Ensure the wallet belongs to the current user
    if wallet.user_id != current_user.id:
        return {"message": "Unauthorized access to this wallet"}, 403

    wallet_card = WalletCard.query.filter_by(wallet_id=wallet.id, card_id=card_id).first()
    if not wallet_card:
        return {"message": "Card not found in this wallet!"}, 404

    return jsonify({
        "id": wallet_card.card.id,
        "name": wallet_card.card.name,
        "nickname": wallet_card.nickname,
        "network": wallet_card.network,
        "issuer": wallet_card.card.issuer,
        "image_url": wallet_card.card.image_url,
        "url": wallet_card.card.url,
    }), 200

# Add a card to the user's wallet
@wallet_routes.route('/cards', methods=["POST"])
@login_required
def add_card():
    """
    Add a card to the user's wallet.
    """
    data = request.json

    # Validate input data (remove 'nickname' from required fields)
    if not data or not all(key in data for key in ["card_id", "network"]):
        return {"message": "Invalid input data"}, 400

    wallet = Wallet.query.filter_by(user_id=current_user.id).first()
    if not wallet:
        return {"message": "Wallet not found!"}, 404

    # Check if the card already exists in the wallet
    existing_wallet_card = WalletCard.query.filter_by(wallet_id=wallet.id, card_id=data["card_id"]).first()
    if existing_wallet_card:
        return {"message": "Card already exists in wallet!"}, 409

    # Check if the card exists in the database
    card = Card.query.get(data["card_id"])
    if not card:
        return {"message": "Card not found!"}, 404

    # Use the provided nickname or default to None
    nickname = data.get("nickname")

    # Add the card to the wallet
    WalletCard.create_wallet_card(wallet.id, data["card_id"], nickname, data["network"])

    return jsonify({"message": "Card added to wallet successfully!"}), 201


# Update card details in the wallet
@wallet_routes.route('/cards/<int:card_id>', methods=["PUT"])
@login_required
def update_card(card_id):
    wallet = Wallet.query.filter_by(user_id=current_user.id).first()
    if not wallet:
        return {"message": "Wallet not found!"}, 404

    wallet_card = WalletCard.query.filter_by(wallet_id=wallet.id, card_id=card_id).first()
    if not wallet_card:
        return {"message": "Card not found in wallet!"}, 404

    data = request.json
    if not data:
        return {"message": "No data provided for update"}, 400

    wallet_card.nickname = data.get("nickname", wallet_card.nickname)
    wallet_card.network = data.get("network", wallet_card.network)
    db.session.commit()

    return jsonify(wallet_card.to_dict()), 200


# Remove a card from the wallet
@wallet_routes.route('/cards/<int:card_id>', methods=["DELETE"])
@login_required
def remove_card(card_id):
    """
    Remove a card from the wallet.
    """
    wallet = Wallet.query.filter_by(user_id=current_user.id).first()
    if not wallet:
        return {"message": "Wallet not found!"}, 404

    wallet_card = WalletCard.query.filter_by(wallet_id=wallet.id, card_id=card_id).first()
    if not wallet_card:
        return {"message": "Card not found in wallet!"}, 404

    # Remove the wallet card
    db.session.delete(wallet_card)
    db.session.commit()

    return {"message": "Card successfully removed from wallet"}, 200