from datetime import datetime

from collections import Counter
import urllib2
import json

from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

from config import Config
# todo add timeline for item.
#todo add user last_seen time
#todo add item_read time
#todo save it forever powerful search suggested tags.
#todo add email func
#todo use many to many model between user and item.
#todo add if a user is confirmed.
#todo review length of field.
#todo understand what the lazy in column mean.
# todo add api for cross-platform use.etc: CLI, mobile device, desktop etc;
tag_item = db.Table('tag_item',
                    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
                    db.Column('item_id', db.Integer, db.ForeignKey('items.id'))
)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=64), unique=True, index=True)
    email = db.Column(db.String(length=64), unique=True, index=True)
    password_hash = db.Column(db.String(length=128))
    added_time = db.Column(db.DateTime, default=datetime.utcnow)
    is_confirmed = db.Column(db.Boolean, default=False)
    items = db.relationship('Item', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.name

    @property
    def password(self):
        raise AttributeError('password cant be read')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_tags(self):
        tags = []
        items = self.items
        if not items:
            return None
        else:
            for item in items:
                if item.tags:
                    for tag in item.tags:
                        tags.append(tag.name)
            if not tags:
                return None
            else:
                return Counter(tags).items()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String)
    domain = db.Column(db.String)
    title = db.Column(db.String)
    image = db.Column(db.String)
    author = db.Column(db.String)
    content = db.Column(db.Text)
    added_time = db.Column(db.DateTime, default=datetime.utcnow)
    is_star = db.Column(db.Boolean, default=False)
    is_archive = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tags = db.relationship('Tag', secondary=tag_item, backref=db.backref('items', lazy='dynamic'))

    def __repr__(self):
        return '<Item %r>' % self.id


    #todo use another thread to parse html to make app more responsive.
    def parse_html(self):
        readability_api_url = Config.READABILITY_API_URL
        readability_token = Config.READABILITY_TOKEN
        full_url = readability_api_url.format(self.link, readability_token)
        req = urllib2.urlopen(full_url)
        res = req.read()
        parsed_item = json.loads(res)
        self.domain = parsed_item['domain']
        self.title = parsed_item['title']
        self.image = parsed_item['lead_image_url']
        self.author = parsed_item['author']
        self.content = parsed_item['content']


    # todo add/modify add_tags fun.
    def add_tags(self):
        pass


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=64))

    def __repr__(self):
        return '<Tag %r>' % self.name
