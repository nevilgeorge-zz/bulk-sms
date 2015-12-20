# forms.py
from flask.ext.wtf import Form
from wtforms import FileField, SelectMultipleField, StringField, TextAreaField
from wtforms.validators import DataRequired

class SendMessageForm(Form):

    """Form used to send a message to a subscription."""

    message_text = TextAreaField('message_text', validators=[DataRequired()])
    subs = ['Hackers', 'Mentors', 'Judges']
    subscriptions = SelectMultipleField(
        'subscriptions',
        choices=[(s.lower(), s) for s in subs],
        validators=[DataRequired()]
    )


class AddToNumberForm(Form):

    """Form used to add a new to/from number."""

    to_number = StringField('to_number')


class AddFromNumberForm(Form):

    """Form used to add a new to/from number."""

    from_number = StringField('from_number')


class UploadFileForm(Form):

    """Form used to upload a csv/txt file of numbers."""

    number_file = FileField('Number File')
