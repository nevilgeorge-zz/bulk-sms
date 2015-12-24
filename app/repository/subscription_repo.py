# subscription_repo.py
from app import db, models
from app.exceptions.duplicate_error import DuplicateError

from sqlalchemy.exc import IntegrityError


def get_all():
    """Return all subscription entities."""
    return models.Subscription.query.all()


def create_one(**kwargs):
    """Create a subscription from kwargs."""
    sub = models.Subscription(**kwargs)
    db.session.add(sub)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise DuplicateError('Subscription already exists!')
