# subscription_repo.py
from sqlalchemy.exc import IntegrityError

from app import db, models
from app.exceptions.duplicate_error import DuplicateError


def create_one(**kwargs):
    """Create Subscription entity from kwargs."""
    sub = models.Subscription(**kwargs)
    db.session.add(sub)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise DuplicateError('Subscription already exists!')


def get_all():
    """Return all Subscription entities."""
    return models.Subscription.query.all()


def get_by_id(subscription_id):
    """Return Subscription entity with given subscription_id."""
    subscription = models.Subscription.query.filter_by(id=subscription_id).first()
    return subscription
