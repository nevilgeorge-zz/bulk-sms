# number_repo.py
from app import db, models
from app.exceptions.duplicate_error import DuplicateError

from sqlalchemy.exc import IntegrityError


def create_one(**kwargs):
    """Create number using kwargs."""

    number = models.Number(**kwargs)
    db.session.add(number)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise DuplicateError('Number already exists!')
