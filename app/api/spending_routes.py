from flask import Blueprint, jsonify, request, render_template
from flask_login import login_required, current_user
from app.models import Spending, SpendingCategory, Category, db
from app.forms import AddCategoryToSpendingForm

spending_routes = Blueprint('spendings', __name__)

# Helper function to format category details
def format_category(spending_category):
    return {
        "category_id": spending_category.category.id,
        "spending_id": spending_category.spending_id,
        "name": spending_category.category.name,
        "parent_categories_id": spending_category.category.parent_category_id,
    }

# Get current user's spending profile
@spending_routes.route('/session', methods=["GET"])
@login_required
def get_current_user_spending():
    spending = Spending.query.filter_by(user_id=current_user.id).first()
    if not spending:
        return {"message": "Spending profile not found!"}, 404

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

# Get all categories for dropdown population
@spending_routes.route('/categories/form', methods=["GET"])
@login_required
def get_add_category_form():
    """
    Return all categories for dynamically populating the dropdown.
    """
    categories = Category.query.all()
    form = AddCategoryToSpendingForm()
    form.category_id.choices = [(category.id, category.name) for category in categories]

    # Serialize the choices for the frontend
    return jsonify({
        "choices": form.category_id.choices
    })

# Get details of a specific category in spending
@spending_routes.route('/categories/<int:category_id>', methods=["GET"])
@login_required
def get_category_in_spending(category_id):
    spending = Spending.query.filter_by(user_id=current_user.id).first()
    if not spending:
        return {"message": "Spending profile not found!"}, 404

    spending_category = SpendingCategory.query.filter_by(
        spending_id=spending.id,
        category_id=category_id
    ).first()

    if not spending_category:
        return {"message": "Category not found in spending profile!"}, 404

    return jsonify(format_category(spending_category)), 200

# Add a category to spending
@spending_routes.route('/categories', methods=["POST"])
@login_required
def add_category_to_spending():
    """
    Add a category to the user's spending profile via API.
    """
    data = request.get_json()
    category_id = data.get("category_id")

    # Validate input
    if not category_id:
        return {"message": "Category ID is required"}, 400

    # Get the user's spending profile
    spending = Spending.query.filter_by(user_id=current_user.id).first()
    if not spending:
        return {"message": "Spending profile not found!"}, 404

    # Validate category existence
    category = Category.query.get(category_id)
    if not category:
        return {"message": "Category not found!"}, 404

    # Check if category already exists in spending
    existing_category_ids = {sc.category_id for sc in spending.categories}
    if category.id in existing_category_ids:
        return {"message": "Category already exists in spending profile!"}, 409

    # Add the category
    try:
        new_spending_category = SpendingCategory(
            spending_id=spending.id,
            category_id=category.id
        )
        db.session.add(new_spending_category)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error adding category to spending: {e}")  # Log the error
        return {"message": "Failed to add category to spending."}, 500

    # Return success response
    return jsonify({
        "message": "Category added successfully",
        "category": format_category(new_spending_category)
    }), 201


# Delete a category from spending
@spending_routes.route('/categories/<int:category_id>', methods=["DELETE"])
@login_required
def delete_category_from_spending(category_id):
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
