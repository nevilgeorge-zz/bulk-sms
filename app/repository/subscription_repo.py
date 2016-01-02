# subscription_repo.py
from sqlalchemy.exc import IntegrityError

from app import db, models
from app.exceptions.duplicate_error import DuplicateError


# core functions
def create_one(**kwargs):
    """Create Subscription entity from kwargs."""
    subscription = models.Subscription(**kwargs)
    db.session.add(subscription)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise DuplicateError('Subscription already exists!')

    return subscription


def get_all():
    """Return all Subscription entities."""
    return models.Subscription.query.all()


def get_by_id(subscription_id):
    """Return Subscription entity with given subscription_id."""
    subscription = models.Subscription.query.filter_by(id=subscription_id).first()
    return subscription


def get_many_by_kwargs(**kwargs):
    """Return all Subscription entities by given kwargs."""
    subscriptions = models.Subscription.query.filter_by(**kwargs).all()
    return subscriptions


def get_one_by_kwargs(**kwargs):
    """Return first Subscription entity by given kwargs."""
    subscription = models.Subscription.query.filter_by(**kwargs).first()
    return subscription
