from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class EditNotesForm(FlaskForm):
    notes = StringField(
        'Notes',
        validators=[
            Optional(strip_whitespace=True),  # Allow optional notes but strip whitespace
            Length(max=255, message='Notes must not exceed 255 characters.')  # Restrict length
        ]
    )
    submit = SubmitField('Update Notes')
