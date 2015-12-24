# models.py
from app import db
import datetime

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300), index=True, unique=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    sent_at = db.Column(db.DateTime)
    # one message has one subscription
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscription.id'))


class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), index=True, unique=True)
    messages_count = db.Column(db.Integer, index=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    # one subscription, many numbers
    numbers = db.relationship('Number', backref='subscription', lazy='dynamic')


class Number(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String, index=True, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    # one number in one subscription
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscription.id'))
    sender_id = db.Column(db.Integer, db.ForeignKey('sender.id'))


class Sender(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numbers = db.relationship('Number', backref='author', lazy='dynamic')
