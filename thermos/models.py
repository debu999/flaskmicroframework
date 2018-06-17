from datetime import datetime

from sqlalchemy.orm.exc import NoResultFound

from thermos import db
from sqlalchemy import desc
from flask_login import UserMixin, current_user
from werkzeug.security import check_password_hash, generate_password_hash

# Junction Table for many to many relationships
tags = db.Table('bookmark_tag',
                db.Column("tag_id", db.Integer, db.ForeignKey("tag.id")),
                db.Column("bookmark_id", db.Integer, db.ForeignKey("bookmark.id")))

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(300))
    bkmrkusername = db.Column(db.String(400))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    _tags = db.relationship("Tag", secondary=tags, backref=db.backref("bookmarks", lazy="dynamic"))

    @property
    def tags(self):
        return ",".join([t.name for t in self._tags])

    @tags.setter
    def tags(self, string):
        if string:
            self._tags = [Tag.get_or_create(name) for name in string.split(",")]


    @classmethod
    def newbookmarks(cls, num):
        return cls.query.filter_by(user=current_user).order_by(desc(cls.date)).limit(num)

    def __repr__(self):
        return "<Bookmark '{}': '{}'>".format(self.url, self.description)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String, nullable=False)
    bookmarks = db.relationship('Bookmark', backref="user", lazy="dynamic")

    def __repr__(self):
        return "<User {}>".format(self.username)

    @property
    def password(self):
        raise AttributeError("Password write-only field")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def _checkpassword(self, password):
        return check_password_hash(self.password_hash, password=password)

    @classmethod
    def getuserbyusername(cls, username):
        return cls.query.filter_by(username=username).first()


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False, unique=True, index=True)


    @classmethod
    def get_or_create(cls, name):
        try:
            return cls.query.filter_by(name=name).one()
        except NoResultFound as exc:
            print("Tag {} is not found in database. Creating new tag.".format(name))
            return cls(name=name)
        except Exception as exc:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(exc).__name__, exc.args)
            print(message)
            raise exc

    def __repr__(self):
        return self.name

