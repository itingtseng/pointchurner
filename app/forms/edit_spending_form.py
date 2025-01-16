from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class EditNotesForm(FlaskForm):
    notes = StringField(
        'Notes',
        validators=[
            DataRequired(message='Notes field is required.'),
            Length(max=255, message='Notes must not exceed 255 characters.')
        ]
    )
    submit = SubmitField('Update Notes')