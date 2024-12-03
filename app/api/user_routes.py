from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import User, db
from app.aws_helpers import remove_file_from_s3
from app.forms import EditProfileForm

user_routes = Blueprint('users', __name__)


@user_routes.route('/')
def users():
    """
    Query for all users and return them in a list of user dictionaries
    """
    users = User.query.all()
    return {'users': [user.to_dict() for user in users]}


@user_routes.route('/<int:id>')
def user(id):
    """
    Query for a user by id and return that user in a dictionary
    """
    user = User.query.get(id)
    if not user:
        return {"message": "User not found"}, 404
    return user.to_dict()


@user_routes.route('/session')
@login_required
def session_user():
    """
    Query for the currently authenticated user and return their information
    """
    if current_user.is_authenticated:
        return current_user.to_dict()
    return {'errors': {'message': 'Unauthorized'}}, 401


@user_routes.route('/me', methods=['DELETE'])
@login_required
def delete_current_user():
    """
    Delete the currently authenticated user and associated resources
    """
    user = User.query.get(current_user.id)

    if not user:
        return {"message": "User not found"}, 404

    # Remove profile and banner images from S3 if they exist
    if user.profileImageUrl:
        remove_file_from_s3(user.profileImageUrl)
    if user.bannerImageUrl:
        remove_file_from_s3(user.bannerImageUrl)

    # Delete user from the database
    db.session.delete(user)
    db.session.commit()

    return {"message": "User deleted successfully."}, 204


@user_routes.route('/session', methods=['PUT'])
@login_required
def edit_current_user():
    """
    Edit the profile of the currently authenticated user
    """
    form = EditProfileForm()
    form["csrf_token"].data = request.cookies.get("csrf_token")

    if form.validate_on_submit():
        # Update user fields
        current_user.username = form.username.data
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.email = form.email.data

        # Commit changes
        db.session.commit()

        return {
            "message": "Profile updated successfully.",
            "user": current_user.to_dict()
        }

    if form.errors:
        return {"errors": form.errors}, 400

    return {"errors": "Invalid request"}, 400
