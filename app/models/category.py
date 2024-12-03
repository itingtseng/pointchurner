from .db import db
from .db import environment, SCHEMA
from ..utils import add_prefix_for_prod



class Category(db.Model):
    __tablename__ = 'categories'

    if environment == "production":
        __table_args__ = {'schema': SCHEMA}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)  # Ensures unique category names
    parent_category_id = db.Column(db.Integer, db.ForeignKey(add_prefix_for_prod('categories.id')), nullable=True)

    # Relationships
    reward_points = db.relationship('RewardPoint', back_populates='category', cascade='all, delete-orphan')
    spending_categories = db.relationship('SpendingCategory', back_populates='category', cascade='all, delete-orphan')
    subcategories = db.relationship(
        'Category',
        backref=db.backref('parent_category', remote_side=[id]),
        cascade='all, delete-orphan'
    )

    def to_dict(self):
        """
        Returns a dictionary representation of a Category instance.
        """
        return {
            'id': self.id,
            'name': self.name,
            'parent_category_id': self.parent_category_id,
            'reward_points': [reward_point.to_dict() for reward_point in self.reward_points] if self.reward_points else [],
            'spending_categories': [sc.to_dict() for sc in self.spending_categories] if self.spending_categories else [],
            'subcategories': [subcategory.to_dict() for subcategory in self.subcategories] if self.subcategories else []
        }

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
