from app.models.db import db, environment, SCHEMA
from datetime import datetime
from ..utils import add_prefix_for_prod


class Wallet(db.Model):
    __tablename__ = 'wallets'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    name = db.Column(db.String(255), nullable=True)  # Optional wallet name
    balance = db.Column(db.Float, nullable=False, default=0.0)  # Added balance field
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='wallets')
    wallet_cards = db.relationship('WalletCard', back_populates='wallet', cascade='all, delete-orphan')

    def to_dict(self, include_wallet_cards=True):
        """
        Returns a dictionary representation of a Wallet instance.

        :param include_wallet_cards: If True, includes details of the associated wallet cards.
        """
        wallet_dict = {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'balance': self.balance,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

        if include_wallet_cards:
            wallet_dict['wallet_cards'] = [wallet_card.to_dict() for wallet_card in self.wallet_cards]

        return wallet_dict
