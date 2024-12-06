from .db import db, environment, SCHEMA
from ..utils import add_prefix_for_prod


class Category(db.Model):
    __tablename__ = 'categories'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)  # Ensures unique category names
    parent_category_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('categories.id')), nullable=True)

    # Relationships
    reward_points = db.relationship(
        'RewardPoint',
        back_populates='category',
        cascade='all, delete-orphan',
        lazy='joined'
    )
    spending_categories = db.relationship(
        'SpendingCategory',
        back_populates='category',
        cascade='all, delete-orphan',
        lazy='joined'
    )
    subcategories = db.relationship(
        'Category',
        backref=db.backref('parent_category', remote_side=[id]),
        cascade='all, delete-orphan',
        lazy='joined'
    )

    def to_dict(self, include_reward_points=False, include_spending_categories=False, include_subcategories=False):
        """
        Returns a dictionary representation of a Category instance.

        :param include_reward_points: If True, includes related reward points.
        :param include_spending_categories: If True, includes related spending categories.
        :param include_subcategories: If True, includes related subcategories.
        """
        category_dict = {
            'id': self.id,
            'name': self.name,
            'parent_category_id': self.parent_category_id,
        }

        if include_reward_points:
            category_dict['reward_points'] = [rp.to_dict() for rp in self.reward_points]

        if include_spending_categories:
            category_dict['spending_categories'] = [sc.to_dict() for sc in self.spending_categories]

        if include_subcategories:
            category_dict['subcategories'] = [subcategory.to_dict() for subcategory in self.subcategories]

        return category_dict

    @staticmethod
    def get_all_categories_with_subcategories():
        """
        Fetch all categories along with their subcategories.
        """
        from sqlalchemy.orm import joinedload
        return db.session.query(Category).options(joinedload(Category.subcategories)).all()

    @staticmethod
    def get_category_by_name(name):
        """
        Fetch a category by its name.
        """
        return Category.query.filter_by(name=name).first()

    @staticmethod
    def create_category(name, parent_category_id=None):
        """
        Create a new category.

        :param name: Name of the category.
        :param parent_category_id: ID of the parent category if applicable.
        """
        category = Category(name=name, parent_category_id=parent_category_id)
        db.session.add(category)
        db.session.commit()
        return category
