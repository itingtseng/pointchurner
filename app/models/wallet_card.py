from app.models.db import db
from datetime import datetime


class WalletCard(db.Model):
    __tablename__ = 'wallet_cards'

    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallets.id', ondelete="CASCADE"), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id', ondelete="CASCADE"), nullable=False)
    nickname = db.Column(db.String(255), nullable=True)
    network = db.Column(db.String(255), nullable=True)  # Added network column
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    wallet = db.relationship('Wallet', back_populates='wallet_cards')
    card = db.relationship('Card', back_populates='wallet_cards')

    def to_dict(self):
        return {
            'id': self.id,
            'wallet_id': self.wallet_id,
            'card_id': self.card_id,
            'nickname': self.nickname,
            'network': self.network,  # Include network in the dictionary
            'created_at': self.created_at,
            'card_details': self.card.to_dict() if self.card else None,
        }
