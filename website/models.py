from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    concept = db.Column(db.String(10000))
    data = db.Column(db.String(10000))
    month = db.Column(db.String(30))

    isExpense = db.Column(db.Boolean)
    amount = db.Column(db.Integer)
    day = db.Column(db.String(3))

    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    transactions = db.relationship("Transaction")
