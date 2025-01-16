from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length

class AddCategoryToSpendingForm(FlaskForm):
    category_id = SelectField(
        'Category',
        coerce=int,  # Ensures the value is coerced to an integer
        validators=[
            DataRequired(message='Please select a category.')
        ]
    )
    notes = StringField(
        'Notes',
        validators=[
            Length(max=255, message='Notes must not exceed 255 characters.')
        ]
    )
    submit = SubmitField('Add Category')
