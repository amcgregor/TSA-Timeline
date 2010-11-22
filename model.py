# encoding: utf-8

import pytz

from datetime import datetime

import mongoengine as db


connection = db.connect('tsa')
log = __import__('logging').getLogger(__name__)
__all__ = ['FeedSearch', 'Feed', 'Story']



class FeedSearch(db.EmbeddedDocument):
    attribute = db.StringField(max_length=64)
    value = db.StringField(max_length=64)


class Feed(db.Document):
    meta = dict(
            collection="feeds",
            ordering=['title'],
            indexes=['name', 'title', 'modified', '-updated']
        )
    
    id = db.ObjectIdField('_id')
    
    name = db.StringField(max_length=250)
    title = db.StringField(max_length=250)
    site = db.URLField(verify_exists=True)
    url = db.URLField(verify_exists=True)
    enabled = db.BooleanField(default=False)
    
    search = db.EmbeddedDocumentField(FeedSearch, default=None)
    
    feed = db.DictField(default=None)
    
    created = db.DateTimeField(default=lambda: datetime.utcnow().replace(microsecond=0))
    modified = db.DateTimeField(default=None)
    updated = db.DateTimeField(default=None)


class Story(db.Document):
    meta = dict(
            collection="stories",
            ordering=['date'],
            indexes=['date', 'feed', 'visible', 'votes']
        )
    
    id = db.ObjectIdField('_id')
    feed = db.ReferenceField(Feed, default=None)
    date = db.DateTimeField(default=lambda: datetime.utcnow().replace(microsecond=0))
    visible = db.BooleanField(default=True)
    votes = db.ListField(db.StringField(max_length=64), default=[])
    
    entry = db.DictField(default=None)
    
    url = db.URLField(verify_exists=True)
    title = db.StringField(max_length=250)
    description = db.StringField(default=None)
    geo = db.GeoPointField(default=None)
