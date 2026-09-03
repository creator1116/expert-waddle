from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from slugify import slugify

from flask import current_app

db = SQLAlchemy()

class Collection(db.Model):
    __tablename__ = 'collections'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text)
    visibility = db.Column(db.String(20), default='public')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    links = db.relationship('CollectionLink', back_populates='collection', cascade='all, delete-orphan', order_by='CollectionLink.position')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'description': self.description,
            'visibility': self.visibility,
            'links': [cl.link.to_dict() for cl in self.links]
        }

class Link(db.Model):
    __tablename__ = 'links'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    url = db.Column(db.String(2000), nullable=False)
    description = db.Column(db.Text)
    tags = db.Column(db.String(250))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'description': self.description,
            'tags': self.tags
        }

class CollectionLink(db.Model):
    __tablename__ = 'collection_links'
    id = db.Column(db.Integer, primary_key=True)
    collection_id = db.Column(db.Integer, db.ForeignKey('collections.id', ondelete='CASCADE'), nullable=False)
    link_id = db.Column(db.Integer, db.ForeignKey('links.id', ondelete='CASCADE'), nullable=False)
    position = db.Column(db.Integer, default=0)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    collection = db.relationship('Collection', back_populates='links')
    link = db.relationship('Link')
