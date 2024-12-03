from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import Card, db
from app.forms import NewCardForm, EditCardForm

card_routes = Blueprint('cards', __name__)

# Get all cards
@card_routes.route('/')
def all_cards():
    """
    Retrieve all cards.
    """
    cards = Card.query.all()
    all_cards = {
        "cards": [
            {
                "id": card.id,
                "name": card.name,
                "issuer": card.issuer,
                "image_url": card.image_url,
                "url": card.url
            }
            for card in cards
        ]
    }
    return jsonify(all_cards)

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
        "issuer": card.issuer,
        "image_url": card.image_url,
        "url": card.url,
        "reward_points": [
            {
                "category_id": reward.category_id,
                "bonus_point": reward.bonus_point,
                "multiplier_type": reward.multiplier_type
            }
            for reward in card.reward_points
        ]
    }
    return jsonify(card_details)

# Create a new card
@card_routes.route('/', methods=["POST"])
@login_required
def create_card():
    """
    Create a new card (admin functionality).
    """
    form = NewCardForm()
    form['csrf_token'].data = request.cookies.get('csrf_token')

    if form.validate_on_submit():
        new_card = Card(
            name=form.name.data,
            issuer=form.issuer.data,
            image_url=form.image_url.data,
            url=form.url.data
        )

        db.session.add(new_card)
        db.session.commit()
        return jsonify(new_card.to_dict()), 201

    return {"errors": form.errors}, 400

# Update an existing card
@card_routes.route('/<int:cardId>', methods=["PUT"])
@login_required
def update_card(cardId):
    """
    Update an existing card (admin functionality).
    """
    card = Card.query.get(cardId)
    if not card:
        return {"message": "Card not found!"}, 404

    form = EditCardForm()
    form['csrf_token'].data = request.cookies.get('csrf_token')

    if form.validate_on_submit():
        card.name = form.name.data
        card.issuer = form.issuer.data
        card.image_url = form.image_url.data
        card.url = form.url.data

        db.session.commit()
        return jsonify(card.to_dict()), 200

    return {"errors": form.errors}, 400

# Delete a card
@card_routes.route('/<int:cardId>', methods=["DELETE"])
@login_required
def delete_card(cardId):
    """
    Delete a card (admin functionality).
    """
    card = Card.query.get(cardId)
    if not card:
        return {"message": "Card not found!"}, 404

    db.session.delete(card)
    db.session.commit()
    return {"message": "Card successfully deleted"}, 200
