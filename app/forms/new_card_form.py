from flask_wtf import FlaskForm
from wtforms import SelectField, StringField
from wtforms.validators import DataRequired, Length

class NewCardForm(FlaskForm):
    card_id = SelectField(
        'card_id',
        choices=[],  # Choices will be populated dynamically from the database or API
        validators=[
            DataRequired(message='Please select a card from the list.')
        ]
    )
    network = SelectField(
        'network',
        choices=[
            ('VISA', 'Visa'),
            ('MASTERCARD', 'MasterCard'),
            ('AMERICAN_EXPRESS', 'American Express'),
            ('DISCOVER', 'Discover'),
            ('OTHER', 'Other')
        ],
        validators=[
            DataRequired(message='Please select a network.')
        ]
    )
    nickname = StringField(
        'nickname',
        validators=[
            DataRequired(message='Please enter a nickname for the card.'),
            Length(max=50, message='Nickname must be less than 50 characters.')
        ]
    )
