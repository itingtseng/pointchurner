from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.forms import AddCategoryToSpendingForm
from app.models import Spending, SpendingCategory, Category, db

spending_routes = Blueprint('spendings', __name__)

# Helper function to format category details
def format_category(spending_category):
    return {
        "category_id": spending_category.category.id,
        "spending_id": spending_category.spending_id,
        "name": spending_category.category.name,
        "parent_categories_id": spending_category.category.parent_category_id,
    }

# Get spending by ID (Optional: Ensure the spending belongs to the current user)
@spending_routes.route('/<int:spending_id>', methods=["GET"])
@login_required
def get_spending_by_id(spending_id):
    """
    Retrieve a spending by its ID and associated categories.
    """
    spending = Spending.query.get(spending_id)
    if not spending:
        return {"message": "Spending not found!"}, 404

    # Ensure the spending belongs to the current user
    if spending.user_id != current_user.id:
        return {"message": "Unauthorized access to this spending"}, 403

    spending_details = {
        "id": spending.id,
        "user_id": spending.user_id,
        "created_at": spending.created_at.isoformat(),
        "updated_at": spending.updated_at.isoformat(),
        "categories": [
            format_category(sc) for sc in spending.categories
        ],
    }
    return jsonify(spending_details), 200

# Get details of a specific category in a spending
@spending_routes.route('/<int:spending_id>/categories/<int:category_id>', methods=["GET"])
@login_required
def get_category_in_spending(spending_id, category_id):
    """
    Get details of a specific category in a spending by spending ID and category ID.
    """
    spending = Spending.query.get(spending_id)
    if not spending:
        return {"message": "Spending not found!"}, 404

    # Ensure the spending belongs to the current user
    if spending.user_id != current_user.id:
        return {"message": "Unauthorized access to this spending"}, 403

    spending_category = SpendingCategory.query.filter_by(spending_id=spending.id, category_id=category_id).first()
    if not spending_category:
        return {"message": "Category not found in this spending!"}, 404

    category_details = {
        "category_id": spending_category.category.id,
        "spending_id": spending_category.spending_id,
        "name": spending_category.category.name,
        "parent_categories_id": spending_category.category.parent_category_id,
    }

    return jsonify(category_details), 200

# Add a category to spending via API
@spending_routes.route('/categories', methods=["POST"])
@login_required
def add_category_to_spending():
    """
    Add a category to the user's spending profile via API.
    """
    data = request.get_json()

    # Validate input: Only category_id is required
    category_id = data.get("category_id")
    if not category_id:
        return {"message": "Category ID is required"}, 400

    # Get the user's spending profile
    spending = Spending.query.filter_by(user_id=current_user.id).first()
    if not spending:
        return {"message": "Spending profile not found!"}, 404

    # Validate the category exists
    category = Category.query.get(category_id)
    if not category:
        return {"message": "Category not found!"}, 404

    # Check if the category is already associated with the spending
    existing_spending_category = SpendingCategory.query.filter_by(
        spending_id=spending.id,
        category_id=category.id
    ).first()

    if existing_spending_category:
        return {"message": "Category already exists in spending profile!"}, 409

    # Create the new spending-category association
    new_spending_category = SpendingCategory(
        spending_id=spending.id,
        category_id=category.id
    )
    db.session.add(new_spending_category)
    db.session.commit()

    # Format the response
    category_details = {
        "category_id": category.id,
        "spending_id": spending.id,
        "name": category.name,
        "parent_categories_id": category.parent_category_id
    }

    return jsonify(category_details), 201

# Delete a category from spending
@spending_routes.route('/categories/<int:category_id>', methods=["DELETE"])
@login_required
def delete_category_from_spending(category_id):
    """
    Remove a category from the user's spending profile.
    """
    spending = Spending.query.filter_by(user_id=current_user.id).first()
    if not spending:
        return {"message": "Spending profile not found!"}, 404

    spending_category = SpendingCategory.query.filter_by(
        spending_id=spending.id,
        category_id=category_id
    ).first()

    if not spending_category:
        return {"message": "Category not found in spending profile!"}, 404

    db.session.delete(spending_category)
    db.session.commit()

    return {"message": "Category successfully removed from spending profile"}, 200
