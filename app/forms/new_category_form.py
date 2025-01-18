from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class AddCategoryToSpendingForm(FlaskForm):
    category_id = SelectField(
        'Category',
        coerce=int,  # Ensures the value is coerced to an integer
        validators=[
            DataRequired(message='Please select a category.')  # Ensures a category is selected
        ]
    )
    notes = StringField(
        'Notes',
        validators=[
            Optional(strip_whitespace=True),  # Allows the field to be empty but trims whitespace
            Length(max=255, message='Notes must not exceed 255 characters.')  # Restrict length
        ]
    )
    submit = SubmitField('Add Category')
