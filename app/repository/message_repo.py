# message_repo.py
from sqlalchemy.exc import IntegrityError

from app import db, models
from app.exceptions.duplicate_error import DuplicateError


def create_one(**kwargs):
    """Create Message entity from kwargs."""
    message = models.Message(**kwargs)
    db.session.add(message)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise DuplicateError('Message already exists!')


def get_all():
    """Return all Message entities."""
    return models.Message.query.all()
