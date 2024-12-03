from app.models.db import db, environment, SCHEMA
from datetime import datetime
from ..utils import add_prefix_for_prod


class WalletCard(db.Model):
    __tablename__ = 'wallet_cards'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('wallets.id')), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('cards.id')), nullable=False)
    nickname = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    wallet = db.relationship('Wallet', back_populates='wallet_cards')
    card = db.relationship('Card', back_populates='wallet_cards')

    def to_dict(self, include_card_details=True):
        """
        Returns a dictionary representation of a WalletCard instance.

        :param include_card_details: If True, includes details of the associated card.
        """
        wallet_card_dict = {
            'id': self.id,
            'wallet_id': self.wallet_id,
            'card_id': self.card_id,
            'nickname': self.nickname,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

        if include_card_details:
            wallet_card_dict['card_details'] = self.card.to_dict() if self.card else None

        return wallet_card_dict
