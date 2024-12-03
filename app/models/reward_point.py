from .db import db
from .db import environment, SCHEMA
from .utils import add_prefix_for_prod


class RewardPoint(db.Model):
    __tablename__ = 'reward_points'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('cards.id')), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('categories.id')), nullable=False)
    bonus_point = db.Column(db.Float, nullable=False)
    multiplier_type = db.Column(db.String(10), nullable=False)  # e.g., '%', 'x'

    # Relationships
    card = db.relationship('Card', back_populates='reward_points')
    category = db.relationship('Category', back_populates='reward_points')

    def to_dict(self):
        """
        Returns a dictionary representation of a RewardPoint instance.
        """
        return {
            'id': self.id,
            'card_id': self.card_id,
            'category_id': self.category_id,
            'bonus_point': self.bonus_point,
            'multiplier_type': self.multiplier_type,
            'card': self.card.to_dict() if self.card else None,
            'category': self.category.to_dict() if self.category else None,
        }
