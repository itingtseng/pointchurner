from flask import Blueprint, request, jsonify
from flask_login import login_required
from app.models import Category, db

category_routes = Blueprint('categories', __name__)

# Get all categories
@category_routes.route('/')
def all_categories():
    """
    Retrieve all categories.
    """
    categories = Category.query.all()
    category_list = [
        {
            "id": category.id,
            "name": category.name,
            "createdAt": category.createdAt,
            "updatedAt": category.updatedAt
        }
        for category in categories
    ]
    return jsonify({"categories": category_list})

# Get category details by ID
@category_routes.route('/<int:categoryId>')
def get_category(categoryId):
    """
    Retrieve a single category's details by its ID.
    """
    category = Category.query.get(categoryId)
    if not category:
        return {"message": "Category not found!"}, 404

    category_details = {
        "id": category.id,
        "name": category.name,
        "createdAt": category.createdAt,
        "updatedAt": category.updatedAt
    }
    return jsonify(category_details)

# Create a new category
@category_routes.route('/', methods=["POST"])
@login_required
def create_category():
    """
    Create a new category (admin functionality).
    """
    data = request.get_json()

    # Validate request data
    if not data or not data.get('name'):
        return {"errors": "Category name is required."}, 400

    new_category = Category(
        name=data['name']
    )

    db.session.add(new_category)
    db.session.commit()
    return jsonify(new_category.to_dict()), 201

# Update an existing category
@category_routes.route('/<int:categoryId>', methods=["PUT"])
@login_required
def update_category(categoryId):
    """
    Update an existing category (admin functionality).
    """
    category = Category.query.get(categoryId)
    if not category:
        return {"message": "Category not found!"}, 404

    data = request.get_json()

    # Validate request data
    if not data or not data.get('name'):
        return {"errors": "Category name is required."}, 400

    category.name = data['name']
    db.session.commit()
    return jsonify(category.to_dict()), 200

# Delete a category
@category_routes.route('/<int:categoryId>', methods=["DELETE"])
@login_required
def delete_category(categoryId):
    """
    Delete a category (admin functionality).
    """
    category = Category.query.get(categoryId)
    if not category:
        return {"message": "Category not found!"}, 404

    db.session.delete(category)
    db.session.commit()
    return {"message": "Category successfully deleted"}, 200
