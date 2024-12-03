from app.models.db import db

class SpendingCategory(db.Model):
    __tablename__ = 'spending_categories'

    id = db.Column(db.Integer, primary_key=True)
    spending_id = db.Column(db.Integer, db.ForeignKey('spendings.id', ondelete="CASCADE"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id', ondelete="CASCADE"), nullable=False)
    priority = db.Column(db.Integer, nullable=False)

    # Relationships
    spending = db.relationship('Spending', back_populates='categories')
    category = db.relationship('Category', back_populates='spending_categories')

    def to_dict(self):
        return {
            'id': self.id,
            'spending_id': self.spending_id,
            'category_id': self.category_id,
            'priority': self.priority,
            'category_details': self.category.to_dict() if self.category else None
        }
