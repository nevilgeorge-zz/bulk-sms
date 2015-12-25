# twilio_dispatcher.py
from twilio import TwilioRestException
from twilio.rest import TwilioRestClient

from app.repository import number_repo, sender_repo, subscription_repo
from app import config, utils

class TwilioDispatcher:
    """Sends text messages using Twilio API."""

    def __init__(self):
        self.client = TwilioRestClient(
            config.TWILIO_ACCOUNT_SID,
            config.TWILIO_AUTH_TOKEN
        )


    def send_to_number(self, to_number, text):
        """Send one message to given to_number that already exists in db."""
        # find the associated sender
        normalized = utils.normalize_number(to_number)
        number = number_repo.get_by_kwargs(number=normalized)[0]
        sender = sender_repo.get_by_id(number.sender_id)

        try:
            # send through the sender
            message = self.client.messages.create(
                body=text,
                to=normalized,
                from_=sender.number
            )

        except TwilioRestException as e:
            # better solution to handling exception?
            raise e


    def send_to_subscription(self, subscription_id, text):
        """Send one message to every number in a subscription."""
        senders = sender_repo.get_all()
        failed_list = []

        for sender in senders:
            # get numbers associated with each sender
            # and has given subscription_id
            numbers = number_repo.get_by_kwargs(
                subscription_id=subscription_id,
                sender_id=sender.id
            )

            for number in numbers:
                try:
                    self.send_to_number(number.number, text)

                except TwilioRestException as e:
                    failed_list.append(number)
                    pass

        return failed_list
