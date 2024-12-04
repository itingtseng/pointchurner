from app.models.db import db
from datetime import datetime
from ..utils import add_prefix_for_prod


class Wallet(db.Model):
    __tablename__ = 'wallets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('users.id')), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='wallets')
    wallet_cards = db.relationship('WalletCard', back_populates='wallet', cascade='all, delete-orphan')

    def to_dict(self, include_wallet_cards=True):
        wallet_dict = {
            'id': self.id,
            'user_id': self.user_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

        if include_wallet_cards:
            wallet_dict['wallet_cards'] = [wallet_card.to_dict() for wallet_card in self.wallet_cards]

        return wallet_dict
