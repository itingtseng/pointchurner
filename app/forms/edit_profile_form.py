from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class EditProfileForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(message="Username is required."),
            Length(max=50, message="Username must be less than 50 characters.")
        ]
    )
    firstname = StringField(
        'First Name',
        validators=[
            DataRequired(message="First name is required."),
            Length(max=50, message="First name must be less than 50 characters.")
        ]
    )
    lastname = StringField(
        'Last Name',
        validators=[
            DataRequired(message="Last name is required."),
            Length(max=50, message="Last name must be less than 50 characters.")
        ]
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(message="Email is required."),
            Email(message="Please enter a valid email address.")
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message="Password is required."),
            Length(min=6, message="Password must be at least 6 characters long.")
        ]
    )
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(message="Confirm password is required."),
            EqualTo('password', message="Passwords must match.")
        ]
    )
    submit = SubmitField('Update Profile')
