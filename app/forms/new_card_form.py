from flask_wtf import FlaskForm
from wtforms import SelectField, StringField
from wtforms.validators import DataRequired, Length


class AddCardToWalletForm(FlaskForm):
    issuer = SelectField(
        "Issuer",
        choices=[],  # Populated dynamically in the route
        validators=[
            DataRequired(message="Please select an issuer."),
        ],
    )
    card_type = SelectField(
        "Card Type",
        choices=[("business", "Business"), ("personal", "Personal")],
        validators=[
            DataRequired(message="Please select a card type."),
        ],
    )
    network = SelectField(
        "Network",
        choices=[
            ("VISA", "Visa"),
            ("MASTERCARD", "MasterCard"),
            ("AMERICAN_EXPRESS", "American Express"),
            ("DISCOVER", "Discover"),
            ("OTHER", "Other"),
        ],
        validators=[
            DataRequired(message="Please select a network."),
        ],
    )
    nickname = StringField(
        "Nickname",
        validators=[
            DataRequired(message="Please enter a nickname for the card."),
            Length(max=50, message="Nickname must be less than 50 characters."),
        ],
    )
