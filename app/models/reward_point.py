from .db import db
from .db import environment, SCHEMA
from ..utils import add_prefix_for_prod


class RewardPoint(db.Model):
    __tablename__ = 'reward_points'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('cards.id')), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('categories.id')), nullable=False)
    bonus_point = db.Column(db.Numeric(10, 2), nullable=False)  # Changed to Decimal
    multiplier_type = db.Column(db.String(10), nullable=False)  # e.g., '%', 'x'

    # Relationships
    card = db.relationship('Card', back_populates='reward_points')
    category = db.relationship('Category', back_populates='reward_points')

    def to_dict(self, include_card=False, include_category=False):
        """
        Returns a dictionary representation of a RewardPoint instance.

        :param include_card: Include card details if True
        :param include_category: Include category details if True
        """
        reward_point_dict = {
            'id': self.id,
            'card_id': self.card_id,
            'category_id': self.category_id,
            'bonus_point': float(self.bonus_point),  # Ensure compatibility with JSON serialization
            'multiplier_type': self.multiplier_type,
        }

        if include_card and self.card:
            reward_point_dict['card'] = self.card.to_dict()

        if include_category and self.category:
            reward_point_dict['category'] = self.category.to_dict()

        return reward_point_dict

    @staticmethod
    def get_reward_points_by_card(card_id):
        """
        Fetch all reward points for a specific card.
        """
        return RewardPoint.query.filter_by(card_id=card_id).all()

    @staticmethod
    def get_reward_points_by_category(category_id):
        """
        Fetch all reward points for a specific category.
        """
        return RewardPoint.query.filter_by(category_id=category_id).all()
