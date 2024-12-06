from app.models.db import db, environment, SCHEMA
from ..utils import add_prefix_for_prod


class Spending(db.Model):
    __tablename__ = 'spendings'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey(add_prefix_for_prod('users.id'), ondelete="CASCADE"),
        nullable=False
    )
    amount = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)  # Represents the spending amount
    description = db.Column(db.String(255), nullable=True)  # Optional spending description
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now(), onupdate=db.func.now())

    # Relationships
    user = db.relationship('User', back_populates='spendings', lazy='joined')
    categories = db.relationship(
        'SpendingCategory',
        back_populates='spending',
        cascade='all, delete-orphan'
    )

    def to_dict(self, include_user=False, include_categories=False):
        """
        Returns a dictionary representation of a Spending instance.

        :param include_user: Include user details if True.
        :param include_categories: Include spending category details if True.
        """
        spending_dict = {
            'id': self.id,
            'user_id': self.user_id,
            'amount': float(self.amount),  # Ensures compatibility with JSON serialization
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

        if include_user and self.user:
            spending_dict['user_details'] = self.user.to_dict()

        if include_categories:
            spending_dict['categories'] = [
                category.to_dict(include_category=True) for category in self.categories
            ]

        return spending_dict

    @staticmethod
    def create_spending(user_id, amount, description=None):
        """
        Create a new Spending instance.

        :param user_id: ID of the associated user.
        :param amount: Amount spent.
        :param description: Optional description of the spending.
        """
        spending = Spending(
            user_id=user_id,
            amount=amount,
            description=description
        )
        db.session.add(spending)
        db.session.commit()
        return spending

    @staticmethod
    def get_spending_by_user(user_id):
        """
        Fetch all spending entries for a specific user.
        """
        return Spending.query.filter_by(user_id=user_id).all()
