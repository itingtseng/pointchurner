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

    # Relationships
    spendings = db.relationship(
        'Spending',
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

    def to_dict(self, include_spendings=False):
        """
        Returns a dictionary representation of a User instance.

        :param include_spendings: Include associated spendings if True
        """
        user_dict = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
        }

        if include_spendings:
            user_dict['spendings'] = [spending.to_dict() for spending in self.spendings]

        return user_dict

    @staticmethod
    def create_user(username, email, password):
        """
        Create a new user instance.
        """
        new_user = User(
            username=username,
            email=email,
            hashed_password=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user
