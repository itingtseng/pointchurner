from app.models.db import db, environment, SCHEMA
from datetime import datetime
from ..utils import add_prefix_for_prod


class Wallet(db.Model):
    __tablename__ = 'wallets'

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
    user = db.relationship('User', back_populates='wallets', lazy='joined')
    wallet_cards = db.relationship(
        'WalletCard',
        back_populates='wallet',
        cascade='all, delete-orphan',
        lazy='joined'
    )

    def to_dict(self, include_wallet_cards=True):
        """
        Returns a dictionary representation of a Wallet instance.

        :param include_wallet_cards: Include associated wallet cards if True.
        """
        wallet_dict = {
            'id': self.id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

        if include_wallet_cards:
            wallet_dict['wallet_cards'] = [wallet_card.to_dict() for wallet_card in self.wallet_cards]

        return wallet_dict

    @staticmethod
    def create_wallet(user_id):
        """
        Create a new wallet for a specific user.

        :param user_id: ID of the associated user.
        """
        wallet = Wallet(
            user_id=user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(wallet)
        db.session.commit()
        return wallet

    @staticmethod
    def get_by_user_id(user_id):
        """
        Fetch all wallets associated with a specific user ID.
        """
        return Wallet.query.filter_by(user_id=user_id).all()
