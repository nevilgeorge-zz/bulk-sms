# number_repo.py
from sqlalchemy.exc import IntegrityError

from app import db, models
from app.exceptions.duplicate_error import DuplicateError
from app.repository import sender_repo


def create_one(**kwargs):
    """Create number using kwargs."""
    min_sender = sender_repo.get_min_sender()
    kwargs['sender_id'] = min_sender.id if min_sender != None else None
    number = models.Number(**kwargs)
    db.session.add(number)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise DuplicateError('Number already exists!')


def get_all():
    """Return all Number entities."""
    return models.Number.query.all()
