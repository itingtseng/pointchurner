from app.models.db import db
from app.models.db import environment, SCHEMA
from ..utils import add_prefix_for_prod


class SpendingCategory(db.Model):
    __tablename__ = 'spending_categories'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    spending_id = db.Column(
        db.Integer,
        db.ForeignKey(add_prefix_for_prod('spendings.id'), ondelete="CASCADE"),
        nullable=False
    )
    category_id = db.Column(
        db.Integer,
        db.ForeignKey(add_prefix_for_prod('categories.id'), ondelete="CASCADE"),
        nullable=False
    )
    priority = db.Column(db.Integer, nullable=False)

    # Relationships
    spending = db.relationship('Spending', back_populates='categories')
    category = db.relationship('Category', back_populates='spending_categories')

    def to_dict(self, include_spending=False):
        """
        Returns a dictionary representation of a SpendingCategory instance.

        :param include_spending: Include spending details if True
        """
        spending_category_dict = {
            'id': self.id,
            'spending_id': self.spending_id,
            'category_id': self.category_id,
            'priority': self.priority,
            'category_details': self.category.to_dict() if self.category else None
        }

        if include_spending and self.spending:
            spending_category_dict['spending_details'] = self.spending.to_dict()

        return spending_category_dict

    @staticmethod
    def get_by_spending_id(spending_id):
        """
        Fetch all spending categories for a specific spending profile.
        """
        return SpendingCategory.query.filter_by(spending_id=spending_id).all()

    @staticmethod
    def get_by_category_id(category_id):
        """
        Fetch all spending categories associated with a specific category.
        """
        return SpendingCategory.query.filter_by(category_id=category_id).all()
