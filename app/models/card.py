from app.models.db import db, environment, SCHEMA
from ..utils import add_prefix_for_prod

class Card(db.Model):
    __tablename__ = 'cards'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    issuer = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    url = db.Column(db.String(255), nullable=True)

    # Relationships
    reward_points = db.relationship(
        'RewardPoint',
        back_populates='card',
        cascade='all, delete-orphan',
        lazy='joined'
    )
    wallet_cards = db.relationship(
        'WalletCard',
        back_populates='card',
        cascade='all, delete-orphan',
        lazy='joined'
    )

    def to_dict(self, include_wallet_cards=False):
        card_dict = {
            'id': self.id,
            'name': self.name,
            'issuer': self.issuer,
            'image_url': self.image_url,
            'url': self.url,
            'reward_points': [reward_point.to_dict() for reward_point in self.reward_points]
        }

        if include_wallet_cards:
            card_dict['wallet_cards'] = [wallet_card.to_dict() for wallet_card in self.wallet_cards]

        return card_dict

    @staticmethod
    def create_card(name, issuer, image_url=None, url=None):
        card = Card(
            name=name,
            issuer=issuer,
            image_url=image_url,
            url=url
        )
        db.session.add(card)
        db.session.commit()
        return card
