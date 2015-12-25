# sender_repo.py
from sqlalchemy.exc import IntegrityError

from app import db, models
from app.exceptions.duplicate_error import DuplicateError


def create_one(**kwargs):
    """Create Sender entity from kwargs."""
    sender = models.Sender(**kwargs)
    db.session.add(sender)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise DuplicateError('Sender already exists!')


def get_all():
    """Return all Sender entities."""
    return models.Sender.query.all()


def get_min_sender():
    """Return the sender with minimum count of associated numbers."""
    senders = get_all()
    min_sender = min(senders, key=lambda sender: len(sender.numbers.all()))
    return min_sender


def get_by_id(sender_id):
    """Return Sender entity with given sender_id."""
    sender = models.Sender.query.filter_by(id=sender_id).first()
    return sender


def get_by_kwargs(**kwargs):
    """Find Sender entity by given **kwargs and return it."""
    sender = models.Sender.query.filter_by(**kwargs)
    return sender
