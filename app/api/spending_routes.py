from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import Spending, db

spending_routes = Blueprint('spendings', __name__)

# Get all spendings for the current user
@spending_routes.route('/')
@login_required
def all_spendings():
    """
    Retrieve all spending records for the current user.
    """
    spendings = Spending.query.filter_by(userId=current_user.id).all()
    spending_list = [
        spending.to_dict() for spending in spendings
    ]
    return jsonify({"spendings": spending_list})

# Get spending details by ID
@spending_routes.route('/<int:spendingId>')
@login_required
def get_spending(spendingId):
    """
    Retrieve a spending record by its ID.
    """
    spending = Spending.query.get(spendingId)
    if not spending:
        return {"message": "Spending not found!"}, 404

    if spending.userId != current_user.id:
        return {"message": "Unauthorized"}, 403

    return jsonify(spending.to_dict())

# Create a new spending record
@spending_routes.route('/', methods=["POST"])
@login_required
def create_spending():
    """
    Create a new spending record for the current user.
    """
    data = request.get_json()

    # Validate input data
    if not data or not data.get('amount') or not data.get('category') or not data.get('date'):
        return {"errors": "Amount, category, and date are required fields."}, 400

    new_spending = Spending(
        userId=current_user.id,
        amount=data['amount'],
        category=data['category'],
        description=data.get('description'),
        date=data['date']
    )

    db.session.add(new_spending)
    db.session.commit()
    return jsonify(new_spending.to_dict()), 201

# Update an existing spending record
@spending_routes.route('/<int:spendingId>', methods=["PUT"])
@login_required
def update_spending(spendingId):
    """
    Update an existing spending record.
    """
    spending = Spending.query.get(spendingId)
    if not spending:
        return {"message": "Spending not found!"}, 404

    if spending.userId != current_user.id:
        return {"message": "Unauthorized"}, 403

    data = request.get_json()

    # Validate input data
    if not data or not data.get('amount') or not data.get('category') or not data.get('date'):
        return {"errors": "Amount, category, and date are required fields."}, 400

    spending.amount = data['amount']
    spending.category = data['category']
    spending.description = data.get('description')
    spending.date = data['date']

    db.session.commit()
    return jsonify(spending.to_dict()), 200

# Delete a spending record
@spending_routes.route('/<int:spendingId>', methods=["DELETE"])
@login_required
def delete_spending(spendingId):
    """
    Delete a spending record.
    """
    spending = Spending.query.get(spendingId)
    if not spending:
        return {"message": "Spending not found!"}, 404

    if spending.userId != current_user.id:
        return {"message": "Unauthorized"}, 403

    db.session.delete(spending)
    db.session.commit()
    return {"message": "Spending successfully deleted"}, 200
