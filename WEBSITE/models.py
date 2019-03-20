from WEBSITE import db, login_manager
from flask_login import UserMixin
from datetime import datetime

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), unique=False, nullable=False)
    subject = db.Column(db.String(255), unique=False, nullable=True)
    email = db.Column(db.String(255), unique=False, nullable=False)
    content = db.Column(db.String(1000), unique=False, nullable=False)
