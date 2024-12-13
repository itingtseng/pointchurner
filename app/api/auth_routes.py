from flask import Blueprint, request
from app.models import User, Wallet, Spending, db
from app.forms import LoginForm, SignUpForm
from flask_login import current_user, login_user, logout_user, login_required

auth_routes = Blueprint('auth', __name__)

@auth_routes.route('/')
def authenticate():
    """
    Authenticates a user.
    """
    if current_user.is_authenticated:
        user_data = current_user.to_dict()
        
        # Include wallet_id
        wallet = Wallet.query.filter_by(user_id=current_user.id).first()
        user_data['wallet_id'] = wallet.id if wallet else None
        
        # Include spending_id
        spending = Spending.query.filter_by(user_id=current_user.id).first()
        user_data['spending_id'] = spending.id if spending else None
        
        return user_data
    return {'errors': {'message': 'Unauthorized'}}, 401

@auth_routes.route('/login', methods=['POST'])
def login():
    """
    Logs a user in.
    """
    form = LoginForm()
    form['csrf_token'].data = request.cookies.get('csrf_token', '')
    if not form['csrf_token'].data:
        return {'errors': {'message': 'Missing CSRF token'}}, 400
    if form.validate_on_submit():
        user = User.query.filter(User.email == form.data['email']).first()
        if not user or not user.check_password(form.data['password']):
            return {'errors': {'message': 'Invalid credentials'}}, 401
        login_user(user)
        
        # Include wallet_id and spending_id
        user_data = user.to_dict()
        wallet = Wallet.query.filter_by(user_id=user.id).first()
        spending = Spending.query.filter_by(user_id=user.id).first()
        user_data['wallet_id'] = wallet.id if wallet else None
        user_data['spending_id'] = spending.id if spending else None
        
        return user_data
    return form.errors, 401

@auth_routes.route('/logout', methods=['POST'])
@login_required
def logout():
    """
    Logs a user out.
    """
    logout_user()
    return {'message': 'User logged out'}

@auth_routes.route('/signup', methods=['POST'])
def sign_up():
    """
    Creates a new user and logs them in.
    """
    form = SignUpForm()
    form['csrf_token'].data = request.cookies.get('csrf_token', '')
    if not form['csrf_token'].data:
        return {'errors': {'message': 'Missing CSRF token'}}, 400
    if form.validate_on_submit():
        existing_user = User.query.filter((User.email == form.data['email']) | (User.username == form.data['username'])).first()
        if existing_user:
            return {'errors': {'message': 'Email or username already taken'}}, 409
        
        # Create new user
        user = User(
            username=form.data['username'],
            email=form.data['email'],
            password=form.data['password']
        )
        db.session.add(user)
        db.session.commit()
        
        # Create wallet and spending profile for the new user
        wallet = Wallet(user_id=user.id)
        spending = Spending(user_id=user.id)
        db.session.add(wallet)
        db.session.add(spending)
        db.session.commit()
        
        # Log the user in
        login_user(user)
        
        # Include wallet_id and spending_id
        user_data = user.to_dict()
        user_data['wallet_id'] = wallet.id
        user_data['spending_id'] = spending.id
        
        return user_data
    return form.errors, 401

@auth_routes.route('/unauthorized')
def unauthorized():
    """
    Returns unauthorized JSON when flask-login authentication fails.
    """
    return {'errors': {'message': 'Unauthorized'}}, 401
