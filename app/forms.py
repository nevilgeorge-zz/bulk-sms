# forms.py
from app import db, models
from flask.ext.wtf import Form
from wtforms import FileField, SelectMultipleField, StringField, TextAreaField, RadioField
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

    subscriptions = models.Subscription.query.all()
    choices = [(sub.id, sub.title) for sub in subscriptions]
    subscription = RadioField('Subscription', choices=choices)


class AddSenderForm(Form):

    """Form used to add a new to/from number."""

    sender_number = StringField('from_number')


class UploadFileForm(Form):

    """Form used to upload a csv/txt file of numbers."""

    number_file = FileField('Number File')
