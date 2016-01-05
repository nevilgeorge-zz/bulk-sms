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

    return message


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


# additional functions
def get_sent_messages():
    """Return all sent messages."""
    messages = models.Message.query.filter(models.Message.sent_at!=None).all()
    return messages


def get_scheduled_messages():
    """Return all scheduled, but not yet sent, messages."""
    messages = models.Message.query.filter(models.Message.sent_at==None).all()
    return messages


def update_by_id(message_id, **kwargs):
    """Update the attributes in kwargs of the given entity."""
    # get message
    message = models.Message.query.filter_by(id=message_id).first()

    # update message
    for attr, val in kwargs.iteritems():
        setattr(message, attr, val)

    # save message
    db.session.add(message)
    db.session.commit()
