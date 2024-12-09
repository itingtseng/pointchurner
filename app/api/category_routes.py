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