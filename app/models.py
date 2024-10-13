from flask_login import UserMixin
from . import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    rides = db.relationship('Ride', backref='passenger', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Ride(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pickup_location = db.Column(db.String(100), nullable=False)
    dropoff_location = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tariff = db.Column(db.String(50), nullable=False)
    distance = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default="Ordered", nullable=False)

    def __repr__(self):
        return f"Ride('{self.pickup_location}', '{self.dropoff_location}', '{self.date}', '{self.status}')"
