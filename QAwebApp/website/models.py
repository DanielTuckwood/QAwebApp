from enum import unique
from . import db
from flask_login import UserMixin

class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sponsorURN = db.Column(db.String(150))
    case_type = db.Column(db.String(150))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

