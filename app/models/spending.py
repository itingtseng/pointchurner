from .db import db
from datetime import datetime

class Spending(db.Model):
    __tablename__ = 'spendings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    categories = db.relationship('SpendingCategory', back_populates='spending', cascade='all, delete-orphan')
    user = db.relationship('User', back_populates='spendings')  # Updated to match the `spendings` relationship in `User`

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'categories': [category.to_dict() for category in self.categories],
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
