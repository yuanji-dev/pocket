from app import db

tag_item = db.Table('tag_item',
                    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
                    db.Column('item_id', db.Integer, db.ForeignKey('items.id'))
)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=64), unique=True)
    items = db.relationship('Item', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.name


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String)
    #todo add a title?
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
