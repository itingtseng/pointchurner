from .db import db, environment, SCHEMA, add_prefix_for_prod
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)
    firstname = db.Column(db.String(255), nullable=True)  # Added firstname
    lastname = db.Column(db.String(255), nullable=True)   # Added lastname

    # Relationships
    spendings = db.relationship(
        'Spending',
        back_populates='user',
        cascade='all, delete-orphan'
    )
    wallets = db.relationship(
        'Wallet',
        back_populates='user',
        cascade='all, delete-orphan'
    )

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self, include_spendings=False, include_wallets=False):
        """
        Returns a dictionary representation of a User instance.

        :param include_spendings: Include associated spendings if True.
        :param include_wallets: Include associated wallets if True.
        """
        user_dict = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'firstname': self.firstname,  # Include firstname
            'lastname': self.lastname,    # Include lastname
        }

        if include_spendings:
            user_dict['spendings'] = [spending.to_dict() for spending in self.spendings]

        if include_wallets:
            user_dict['wallets'] = [wallet.to_dict() for wallet in self.wallets]

        return user_dict

    @staticmethod
    def create_user(username, email, password, firstname=None, lastname=None):
        """
        Create a new user instance.

        :param username: Username of the new user.
        :param email: Email of the new user.
        :param password: Plaintext password to hash and store.
        :param firstname: First name of the user.
        :param lastname: Last name of the user.
        """
        new_user = User(
            username=username,
            email=email,
            hashed_password=generate_password_hash(password),
            firstname=firstname,
            lastname=lastname
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user
