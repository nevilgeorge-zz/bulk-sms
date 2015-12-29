# message_repo.py
from sqlalchemy.exc import IntegrityError

from app import db, models
from app.exceptions.duplicate_error import DuplicateError


# core functions
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


def get_by_id(message_id):
    """Return Message entity with given message_id."""
    message = models.Message.query.filter_by(id=message_id).first()
    return message


def get_many_by_kwargs(**kwargs):
    """Return all Message entities by given kwargs."""
    messages = models.Message.query.filter_by(**kwargs).all()
    return messages


def get_one_by_kwargs(**kwargs):
    """Return first Message entity by given kwargs."""
    message = models.Message.query.filter_by(**kwargs).first()
    return message
