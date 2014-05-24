from app import db, login_manager
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
#todo item add star, type, archive, etc.
#todo review length of field.

tag_item = db.Table('tag_item',
                    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
                    db.Column('item_id', db.Integer, db.ForeignKey('items.id'))
)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String)
    #add a title?
    title = db.Column(db.String)
    is_star = db.Column(db.Boolean)
    is_archive = db.Column(db.Boolean)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tags = db.relationship('Tag', secondary=tag_item, backref=db.backref('items', lazy='dynamic'))

    def __repr__(self):
        return '<Item %r>' % self.id


class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):
        return '<Tag %r>' % self.name
