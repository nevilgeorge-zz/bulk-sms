# number_repo.py
from app import db, models

def create_one(**kwargs):
    """Create number using kwargs."""

    number = models.Number(**kwargs)
    db.session.add(number)
    db.session.commit()
