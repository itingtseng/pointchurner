from flask_wtf import FlaskForm
from wtforms import SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class NewCategoryForm(FlaskForm):
    category_id = SelectField(
        'Category',
        coerce=int,
        validators=[
            DataRequired(message='Please select a category.')
        ]
    )
    priority = IntegerField(
        'Priority',
        validators=[
            DataRequired(message='Please enter a priority value.'),
            NumberRange(min=1, message='Priority must be greater than or equal to 1.')
        ]
    )
    submit = SubmitField('Add Category')
