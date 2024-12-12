from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Card, Wallet, RewardPoint, Category, db
from app.forms import AddCardToWalletForm, EditCardForm

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

    # Build the card details including category names
    card_details = {
        "id": card.id,
        "name": card.name,
        "issuer": card.issuer,
        "image_url": card.image_url,
        "url": card.url,
        "reward_points": [
            {
                "category_name": reward.category.name,  # Get category name
                "bonus_point": reward.bonus_point,
                "multiplier_type": reward.multiplier_type
            }
            for reward in card.reward_points
        ]
    }
    return jsonify(card_details)

# Add card to wallet via form
@card_routes.route('/wallet/cards/new', methods=['GET', 'POST'])
@login_required
def add_card_to_wallet_form():
    """
    Render a form for adding a card to the wallet and handle submission.
    """
    form = AddCardToWalletForm()
    form.card_id.choices = [(card.id, card.name) for card in Card.query.all()]
    form.wallet_id.choices = [(wallet.id, wallet.name) for wallet in Wallet.query.filter_by(user_id=current_user.id).all()]

    if form.validate_on_submit():
        wallet_id = form.wallet_id.data
        card_id = form.card_id.data
        nickname = form.nickname.data
        network = form.network.data

        # Check if card already exists in the wallet
        existing_card = Wallet.query.filter_by(id=wallet_id).join(Card).filter(Card.id == card_id).first()
        if existing_card:
            flash("Card already exists in the selected wallet!", "error")
            return redirect(url_for("card_routes.add_card_to_wallet_form"))

        # Add the card to the wallet
        new_wallet_card = Wallet(card_id=card_id, wallet_id=wallet_id, nickname=nickname, network=network)
        db.session.add(new_wallet_card)
        db.session.commit()

        flash("Card successfully added to wallet!", "success")
        return redirect(url_for("card_routes.all_cards"))

    return render_template("add_card_form.html", form=form)

# Edit card details in the wallet via form
@card_routes.route('/wallet/cards/<int:cardId>/edit', methods=['GET', 'POST'])
@login_required
def edit_card_form(cardId):
    """
    Render a form to edit card details in the wallet and handle submission.
    """
    wallet_card = Wallet.query.join(Card).filter(Card.id == cardId, Wallet.user_id == current_user.id).first()
    if not wallet_card:
        flash("Card not found in your wallet!", "error")
        return redirect(url_for("card_routes.all_cards"))

    form = EditCardForm(obj=wallet_card)

    if form.validate_on_submit():
        wallet_card.nickname = form.nickname.data
        wallet_card.network = form.network.data
        db.session.commit()

        flash("Card successfully updated!", "success")
        return redirect(url_for("card_routes.all_cards"))

    return render_template("edit_card_form.html", form=form)
