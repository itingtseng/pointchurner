from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import User, Wallet, db
from app.aws_helpers import remove_file_from_s3
from app.forms import EditProfileForm

user_routes = Blueprint('users', __name__)

@user_routes.route('/')
def users():
    """
    Query for all users and return them in a list of user dictionaries.
    """
    users = User.query.all()
    return {'users': [user.to_dict() for user in users]}


@user_routes.route('/<int:id>')
def user(id):
    """
    Query for a user by ID and return that user in a dictionary.
    """
    user = User.query.get(id)
    if not user:
        return {"message": "User not found"}, 404
    return user.to_dict()


@user_routes.route('/session')
@login_required
def sessionUser():
    """
    Query for the currently authenticated user and return their information,
    including wallet ID if available.
    """
    if current_user.is_authenticated:
        user_data = current_user.to_dict()

        # Attach wallet ID if the user has a wallet
        wallet = Wallet.query.filter_by(user_id=current_user.id).first()
        user_data['wallet_id'] = wallet.id if wallet else None

        print("Session user data being returned:", user_data)  # Debug log
        return jsonify(user_data), 200

    return {'errors': {'message': 'Unauthorized'}}, 401


@user_routes.route('/me', methods=['DELETE'])
@login_required
def delete_current_user():
    """
    Delete the currently authenticated user and associated resources.
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
    Edit the profile of the currently authenticated user.
    """
    form = EditProfileForm()
    form["csrf_token"].data = request.cookies.get("csrf_token")

    if form.validate_on_submit():
        # Update user fields
        current_user.username = form.username.data
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.email = form.email.data

        # If password is provided, update it
        if form.password.data:
            current_user.set_password(form.password.data)

        # Commit changes
        db.session.commit()

        return {
            "message": "Profile updated successfully.",
            "user": current_user.to_dict()
        }, 200

    # Handle validation errors
    return {"errors": form.errors}, 400


@user_routes.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_user_form():
    """
    Render and handle submission of the user profile edit form.
    """
    form = EditProfileForm(obj=current_user)  # Pre-fill the form with current user data

    if form.validate_on_submit():
        # Reuse logic from `edit_current_user`
        current_user.username = form.username.data
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.email = form.email.data

        # Update password if provided
        if form.password.data:
            current_user.set_password(form.password.data)

        db.session.commit()

        flash("Profile updated successfully!", "success")
        return redirect(url_for('user_routes.sessionUser'))

    return render_template('edit_profile_form.html', form=form)


@user_routes.route('/wallet/<int:user_id>')
@login_required
def get_user_wallet(user_id):
    """
    Retrieve the wallet for a specific user by ID.
    """
    if current_user.id != user_id:
        return {"errors": "Unauthorized access"}, 403

    wallet = Wallet.query.filter_by(user_id=user_id).first()
    if not wallet:
        return {"message": "Wallet not found"}, 404

    return {"wallet_id": wallet.id, "balance": wallet.balance}, 200
