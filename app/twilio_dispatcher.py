# twilio_dispatcher.py
from twilio import TwilioRestException
from twilio.rest import TwilioRestClient

from app import utils
from app.exceptions.not_found_error import NotFoundError
from app.repository import number_repo, sender_repo, subscription_repo
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN

class TwilioDispatcher:
    """Sends text messages using Twilio API."""

    def __init__(self):
        self.client = TwilioRestClient(
            TWILIO_ACCOUNT_SID,
            TWILIO_AUTH_TOKEN
        )


    def send_to_number(self, to_number, text):
        """Send one message to given to_number that already exists in db."""
        # find the associated sender
        number = number_repo.get_by_number(to_number)
        if not number:
            raise NotFoundError('Number {num} not found'.format(num=to_number))

        sender = sender_repo.get_by_id(number.sender_id)

        try:
            # send through the sender
            message = self.client.messages.create(
                body=text,
                to=number.number,
                from_=sender.number
            )

        except TwilioRestException as e:
            # better solution to handling exception?
            raise e


    def send_to_subscription(self, message):
        """Send one message to every number in a subscription."""
        senders = sender_repo.get_all()
        failed = {}

        for sender in senders:
            # get numbers associated with each sender
            # and has given subscription_id
            numbers = number_repo.get_many_by_kwargs(
                subscription_id=message.subscription_id,
                sender_id=sender.id
            )

            for number in numbers:
                try:
                    self.send_to_number(number.number, message.text)

                except (TwilioRestException, NotFoundError) as e:
                    failed[number.number] = str(e)
                    pass

        return failed
