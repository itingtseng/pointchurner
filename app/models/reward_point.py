from .db import db, environment, SCHEMA
from ..utils import add_prefix_for_prod


class RewardPoint(db.Model):
    __tablename__ = 'reward_points'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('cards.id')), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('categories.id')), nullable=False)
    bonus_point = db.Column(db.Numeric(10, 2), nullable=False)  # Use Decimal for precise numeric handling
    multiplier_type = db.Column(db.String(10), nullable=False)  # Examples: '%', 'x'
    notes = db.Column(db.String(255), nullable=True)  # New notes column with a max length of 255 characters

    # Relationships
    card = db.relationship(
        'Card',
        back_populates='reward_points',
        lazy='joined'
    )
    category = db.relationship(
        'Category',
        back_populates='reward_points',
        lazy='joined'
    )

    def to_dict(self, include_card=False, include_category=False):
        """
        Returns a dictionary representation of a RewardPoint instance.

        :param include_card: Include associated card details if True.
        :param include_category: Include associated category details if True.
        """
        reward_point_dict = {
            'id': self.id,
            'card_id': self.card_id,
            'category_id': self.category_id,
            'bonus_point': float(self.bonus_point),  # Ensure JSON serialization compatibility
            'multiplier_type': self.multiplier_type,
            'notes': self.notes,  # Include the notes field in the dictionary
        }

        if include_card and self.card:
            reward_point_dict['card'] = self.card.to_dict()

        if include_category and self.category:
            reward_point_dict['category'] = self.category.to_dict()

        return reward_point_dict

    @staticmethod
    def get_reward_points_by_card(card_id):
        """
        Fetch all reward points associated with a specific card.
        """
        return RewardPoint.query.filter_by(card_id=card_id).all()

    @staticmethod
    def get_reward_points_by_category(category_id):
        """
        Fetch all reward points associated with a specific category.
        """
        return RewardPoint.query.filter_by(category_id=category_id).all()

    @staticmethod
    def create_reward_point(card_id, category_id, bonus_point, multiplier_type, notes=None):
        """
        Create a new RewardPoint instance.

        :param card_id: ID of the associated card.
        :param category_id: ID of the associated category.
        :param bonus_point: Bonus points for the reward.
        :param multiplier_type: Multiplier type (e.g., '%', 'x').
        :param notes: Optional notes for the reward point.
        """
        reward_point = RewardPoint(
            card_id=card_id,
            category_id=category_id,
            bonus_point=bonus_point,
            multiplier_type=multiplier_type,
            notes=notes  # Set the notes field
        )
        db.session.add(reward_point)
        db.session.commit()
        return reward_point
