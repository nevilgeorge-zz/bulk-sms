from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
sender = Table('sender', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('sender_number', VARCHAR),
)

sender = Table('sender', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('number', String),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['sender'].columns['sender_number'].drop()
    post_meta.tables['sender'].columns['number'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['sender'].columns['sender_number'].create()
    post_meta.tables['sender'].columns['number'].drop()
