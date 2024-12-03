from .db import db, environment, SCHEMA
from ..utils import add_prefix_for_prod
from datetime import datetime


class Spending(db.Model):
    __tablename__ = 'spendings'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey(add_prefix_for_prod('users.id'), ondelete="CASCADE"),
        nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    categories = db.relationship(
        'SpendingCategory',
        back_populates='spending',
        cascade='all, delete-orphan'
    )
    user = db.relationship('User', back_populates='spendings')  # Ensure `spendings` matches the relationship in `User`

    def to_dict(self, include_categories=True):
        """
        Returns a dictionary representation of a Spending instance.

        :param include_categories: Include associated categories if True
        """
        spending_dict = {
            'id': self.id,
            'user_id': self.user_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

        if include_categories:
            spending_dict['categories'] = [category.to_dict() for category in self.categories]

        return spending_dict

    @staticmethod
    def get_by_user_id(user_id):
        """
        Fetch all spending records for a specific user.
        """
        return Spending.query.filter_by(user_id=user_id).all()

    @staticmethod
    def create_spending(user_id):
        """
        Create a new spending profile for a user.
        """
        spending = Spending(user_id=user_id)
        db.session.add(spending)
        db.session.commit()
        return spending
