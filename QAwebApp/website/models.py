from flask_login import UserMixin
from datetime import datetime
from . import db

#Case table model
class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    sponsorURN = db.Column(db.String(150))
    case_type = db.Column(db.String(150))
    txt = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=datetime.now)

#Note table model
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    txt = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=datetime.now)

#User table model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    admin = db.Column(db.Boolean)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    cases = db.relationship('Case')
    notes = db.relationship('Note')