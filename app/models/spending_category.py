from app.models.db import db, environment, SCHEMA
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
    notes = db.Column(db.String(255), nullable=True)  # New notes column

    # Relationships
    spending = db.relationship(
        'Spending',
        back_populates='categories',
        lazy='joined'
    )
    category = db.relationship(
        'Category',
        back_populates='spending_categories',
        lazy='joined'
    )

    def to_dict(self, include_spending=False, include_category=False):
        """
        Returns a dictionary representation of a SpendingCategory instance.

        :param include_spending: Include spending details if True.
        :param include_category: Include category details if True.
        """
        spending_category_dict = {
            'id': self.id,
            'spending_id': self.spending_id,
            'category_id': self.category_id,
            'notes': self.notes  # Include notes in output
        }

        if include_category and self.category:
            spending_category_dict['category_details'] = self.category.to_dict()

        if include_spending and self.spending:
            spending_category_dict['spending_details'] = self.spending.to_dict()

        return spending_category_dict

    @staticmethod
    def get_by_spending_id(spending_id):
        """
        Fetch all spending categories associated with a specific spending ID.
        """
        return SpendingCategory.query.filter_by(spending_id=spending_id).all()

    @staticmethod
    def create_spending_category(spending_id, category_id, notes=None):
        """
        Create a new SpendingCategory instance.

        :param spending_id: ID of the associated spending.
        :param category_id: ID of the associated category.
        :param notes: Optional notes for the category.
        """
        spending_category = SpendingCategory(
            spending_id=spending_id,
            category_id=category_id,
            notes=notes  # Include notes during creation
        )
        db.session.add(spending_category)
        db.session.commit()
        return spending_category