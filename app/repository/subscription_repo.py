# subscription_repo.py
from app import db, models

def get_all():
    """Return all subscription entities."""
    return models.Subscription.query.all()


def create_one(**kwargs):
    """Create a subscription from kwargs."""
    sub = models.Subscription(**kwargs)
    db.session.add(sub)
    db.session.commit()
