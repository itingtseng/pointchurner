from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Optional

class EditCardForm(FlaskForm):
    nickname = StringField(
        'nickname',
        validators=[
            DataRequired(message='Please enter a nickname for the card.'),
            Length(max=100, message='Nickname must be less than 100 characters.')
        ]
    )
    network = SelectField(
        'network',
        choices=[
            ('VISA', 'Visa'),
            ('MASTERCARD', 'MasterCard'),
            ('AMERICAN_EXPRESS', 'American Express'),
            ('DISCOVER', 'Discover'),
        ],
        validators=[
            DataRequired(message='Please select a network.')
        ]
    )
    submit = SubmitField('Update Card')
