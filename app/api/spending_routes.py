from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.forms import AddCategoryToSpendingForm
from app.models import Spending, Category, db

spending_routes = Blueprint('spendings', __name__)

# Helper function to format category details
def format_category(category, spending_id):
    return {
        "category_id": category.id,
        "spending_id": spending_id,
        "name": category.name,
        "parent_categories_id": category.parent_categories_id,
    }

# Get spending details and associated categories
@spending_routes.route('/')
@login_required
def get_spending_categories():
    """
    Retrieve spending details and associated categories for the current user.
    """
    spending = Spending.query.filter_by(userId=current_user.id).first()
    if not spending:
        return {"message": "Spending profile not found!"}, 404

    categories = [
        format_category(category, spending.id) for category in spending.categories
    ]
    return jsonify({"spending_id": spending.id, "categories": categories}), 200

# Add a category to spending via API
@spending_routes.route('/categories', methods=["POST"])
@login_required
def add_category_to_spending():
    """
    Add a category to the user's spending profile via API.
    """
    data = request.get_json()
    if not data or not data.get("category_id"):
        return {"message": "Category ID is required"}, 400

    spending = Spending.query.filter_by(userId=current_user.id).first()
    if not spending:
        return {"message": "Spending profile not found!"}, 404

    category = Category.query.get(data["category_id"])
    if not category:
        return {"message": "Category not found!"}, 404

    if category in spending.categories:
        return {"message": "Category already exists in spending profile!"}, 409

    spending.categories.append(category)
    db.session.commit()

    return jsonify(format_category(category, spending.id)), 201

# Add a category to spending via form
@spending_routes.route('/categories/new', methods=['GET', 'POST'])
@login_required
def add_category_form():
    """
    Render a form for adding a category to spending and handle its submission.
    """
    form = AddCategoryToSpendingForm()
    form.category_id.choices = [(cat.id, cat.name) for cat in Category.query.all()]

    if form.validate_on_submit():
        spending = Spending.query.filter_by(userId=current_user.id).first()
        if not spending:
            flash("Spending profile not found!", "error")
            return redirect(url_for("spending_view"))

        category = Category.query.get(form.category_id.data)
        if not category:
            flash("Category not found!", "error")
            return redirect(url_for("add_category_form"))

        if category in spending.categories:
            flash("Category already exists in your spending profile!", "error")
            return redirect(url_for("spending_view"))

        # Add category to spending
        spending.categories.append(category)
        db.session.commit()

        flash("Category successfully added!", "success")
        return redirect(url_for("spending_view"))

    return render_template("add_category_form.html", form=form)

# Delete a category from spending
@spending_routes.route('/categories/<int:categoryId>', methods=["DELETE"])
@login_required
def delete_category_from_spending(categoryId):
    """
    Remove a category from the user's spending profile.
    """
    spending = Spending.query.filter_by(userId=current_user.id).first()
    if not spending:
        return {"message": "Spending profile not found!"}, 404

    category = Category.query.get(categoryId)
    if not category or category not in spending.categories:
        return {"message": "Category not found in spending profile!"}, 404

    spending.categories.remove(category)
    db.session.commit()

    return {"message": "Category successfully removed from spending profile"}, 200
