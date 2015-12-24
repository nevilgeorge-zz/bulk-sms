from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
number = Table('number', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('number', String),
    Column('created_at', DateTime, default=ColumnDefault(<function <lambda> at 0x101b67848>)),
    Column('subscription_id', Integer),
    Column('sender_id', Integer),
)

sender = Table('sender', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
)

message = Table('message', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('text', VARCHAR(length=300)),
    Column('time_created', DATETIME),
    Column('time_sent', DATETIME),
)

message = Table('message', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('text', String(length=300)),
    Column('created_at', DateTime, default=ColumnDefault(<function <lambda> at 0x101b4de60>)),
    Column('sent_at', DateTime),
    Column('subscription_id', Integer),
)

subscription = Table('subscription', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=32)),
    Column('messages_count', Integer),
    Column('created_at', DateTime, default=ColumnDefault(<function <lambda> at 0x101b67500>)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['number'].create()
    post_meta.tables['sender'].create()
    pre_meta.tables['message'].columns['time_created'].drop()
    pre_meta.tables['message'].columns['time_sent'].drop()
    post_meta.tables['message'].columns['created_at'].create()
    post_meta.tables['message'].columns['sent_at'].create()
    post_meta.tables['message'].columns['subscription_id'].create()
    post_meta.tables['subscription'].columns['created_at'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['number'].drop()
    post_meta.tables['sender'].drop()
    pre_meta.tables['message'].columns['time_created'].create()
    pre_meta.tables['message'].columns['time_sent'].create()
    post_meta.tables['message'].columns['created_at'].drop()
    post_meta.tables['message'].columns['sent_at'].drop()
    post_meta.tables['message'].columns['subscription_id'].drop()
    post_meta.tables['subscription'].columns['created_at'].drop()
