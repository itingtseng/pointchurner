from app.models.db import db, environment, SCHEMA
from datetime import datetime
from ..utils import add_prefix_for_prod


class WalletCard(db.Model):
    __tablename__ = 'wallet_cards'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(
        db.Integer,
        db.ForeignKey(add_prefix_for_prod('wallets.id'), ondelete="CASCADE"),
        nullable=False
    )
    card_id = db.Column(
        db.Integer,
        db.ForeignKey(add_prefix_for_prod('cards.id'), ondelete="CASCADE"),
        nullable=False
    )
    nickname = db.Column(db.String(255), nullable=True)
    network = db.Column(db.String(255), nullable=True)  # Network column
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    wallet = db.relationship('Wallet', back_populates='wallet_cards', lazy='joined')
    card = db.relationship('Card', back_populates='wallet_cards', lazy='joined')

    def to_dict(self, include_wallet=False, include_card=False):
        """
        Returns a dictionary representation of a WalletCard instance.

        :param include_wallet: Include wallet details if True.
        :param include_card: Include card details if True.
        """
        wallet_card_dict = {
            'id': self.id,
            'wallet_id': self.wallet_id,
            'card_id': self.card_id,
            'nickname': self.nickname,
            'network': self.network,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

        if include_card and self.card:
            wallet_card_dict['card_details'] = self.card.to_dict()

        if include_wallet and self.wallet:
            wallet_card_dict['wallet_details'] = self.wallet.to_dict()

        return wallet_card_dict

    @staticmethod
    def create_wallet_card(wallet_id, card_id, nickname=None, network=None):
        """
        Create a new WalletCard instance.

        :param wallet_id: ID of the associated wallet.
        :param card_id: ID of the associated card.
        :param nickname: Optional nickname for the card.
        :param network: Optional network information (e.g., Visa, Mastercard).
        """
        wallet_card = WalletCard(
            wallet_id=wallet_id,
            card_id=card_id,
            nickname=nickname,
            network=network,
            created_at=datetime.utcnow()
        )
        db.session.add(wallet_card)
        db.session.commit()
        return wallet_card

    @staticmethod
    def get_by_wallet_id(wallet_id):
        """
        Fetch all wallet cards associated with a specific wallet ID.
        """
        return WalletCard.query.filter_by(wallet_id=wallet_id).all()
