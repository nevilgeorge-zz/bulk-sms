# number_repo.py
from sqlalchemy.exc import IntegrityError

from app import db, models, utils
from app.exceptions.duplicate_error import DuplicateError
from app.repository import sender_repo


def create_one(**kwargs):
    """Create Number entity using kwargs."""
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


def get_by_number(num):
    """Return Number entity with given number."""
    normalized_number = utils.normalize_number(num)
    number = models.Number.query.filter_by(
        number=normalized_number
    ).first()
    return number


def get_by_kwargs(**kwargs):
    """Find Number entity by given kwargs and return it."""
    numbers = models.Number.query.filter_by(**kwargs).all()
    return numbers
