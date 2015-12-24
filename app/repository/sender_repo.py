# sender_repo.py
from sqlalchemy.exc import IntegrityError

from app import db, models
from app.exceptions.duplicate_error import DuplicateError


def create_one(**kwargs):
    """Create a sender from kwargs."""
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
