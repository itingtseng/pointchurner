from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

class EditCardForm(FlaskForm):
    nickname = StringField(
        'Nickname',
        validators=[
            DataRequired(message='Please enter a nickname for the card.'),
            Length(max=100, message='Nickname must be less than 100 characters.')
        ]
    )
    network = SelectField(
        'Network',
        choices=[
            ('VISA', 'Visa'),
            ('MASTERCARD', 'MasterCard'),
            ('AMERICAN_EXPRESS', 'American Express'),
            ('DISCOVER', 'Discover'),
            ('OTHER', 'Other')  # Added "Other" for flexibility
        ],
        validators=[
            DataRequired(message='Please select a network.')
        ]
    )
    submit = SubmitField('Update Card')
