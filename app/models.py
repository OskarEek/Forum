from . import db, login
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash




class Item(db.Model):
    """List item."""
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    description = db.Column(db.String(64))
    done = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Item: {} - {}>'.format(self.id, self.title)

class User(UserMixin, db.Model):
    """Application user."""
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64))
    password_hash = db.Column(db.String(64))
    posts = db.relationship('Item', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
