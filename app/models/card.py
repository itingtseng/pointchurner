from .db import db
from .db import environment, SCHEMA
from ..utils import add_prefix_for_prod


class Card(db.Model):
    __tablename__ = 'cards'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)  # Ensuring unique card names
    issuer = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False, unique=True)  # Ensuring unique URLs

    # Relationships
    reward_points = db.relationship('RewardPoint', back_populates='card', cascade='all, delete-orphan')

    def to_dict(self):
        """
        Returns a dictionary representation of a Card instance.
        """
        return {
            'id': self.id,
            'name': self.name,
            'issuer': self.issuer,
            'image_url': self.image_url,
            'url': self.url,
            'reward_points': [reward_point.to_dict() for reward_point in self.reward_points]
        }

    @staticmethod
    def query_with_reward_points():
        """
        Query cards with eager loading of reward points to optimize performance.
        """
        from sqlalchemy.orm import joinedload
        return db.session.query(Card).options(joinedload(Card.reward_points))
