from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

class AddCategoryToSpendingForm(FlaskForm):
    category_id = SelectField(
        'Category',
        coerce=int,  # Ensures the value is coerced to an integer
        validators=[
            DataRequired(message='Please select a category.')
        ]
    )
    submit = SubmitField('Add Category')
