# forms.py
from flask.ext.wtf import Form
from wtforms import FileField, SelectMultipleField, StringField, TextAreaField, RadioField, SelectField, DateTimeField
from wtforms.validators import DataRequired

from app import db, models
from app.repository import subscription_repo

class SendMessageForm(Form):
    """Form used to send a message to a subscription."""

    message_text = TextAreaField('message_text', validators=[DataRequired()])
    subs = subscription_repo.get_all()
    choices = [(str(sub.id), sub.title) for sub in subs]
    subscription = SelectField(
        'subscription',
        choices=choices,
        validators=[DataRequired()]
    )


class ScheduleMessageForm(Form):
    """Form used to schedule a message to send at a given time."""

    message_text = TextAreaField('message_text', validators=[DataRequired()])
    subs = subscription_repo.get_all()
    choices = [(str(sub.id), sub.title) for sub in subs]
    subscription = SelectField(
        'subscription',
        choices=choices,
        validators=[DataRequired()]
    )
    send_time = DateTimeField('send_time', format='%m/%d/%Y %I:%M %p')


class AddNumberForm(Form):
    """Form used to add a new to/from number."""

    number = StringField('Number', validators=[DataRequired()])

    subscriptions = subscription_repo.get_all()
    choices = [(str(sub.id), sub.title) for sub in subscriptions]
    subscription = SelectField('Subscription', choices=choices, validators=[DataRequired()])


class AddSenderForm(Form):
    """Form used to add a new to/from number."""

    sender_number = StringField('from_number', validators=[DataRequired()])


class UploadFileForm(Form):
    """Form used to upload a csv/txt file of numbers."""

    number_file = FileField('Number File', validators=[DataRequired()])

    subscriptions = subscription_repo.get_all()
    choices = [(str(sub.id), sub.title) for sub in subscriptions]
    subscription = SelectField('Subscription', choices=choices, validators=[DataRequired()])


class AddSubscriptionForm(Form):
    """Form used to create a new subscription."""

    title = StringField('name', validators=[DataRequired()])
