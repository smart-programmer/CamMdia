from WEBSITE import db, login_manager
from flask_login import UserMixin
from datetime import datetime

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), unique=False, nullable=False)
    subject = db.Column(db.String(255), unique=False, nullable=True)
    email = db.Column(db.String(255), unique=False, nullable=False)
    content = db.Column(db.String(1500), unique=False, nullable=False)
    state = db.Column(db.String(20), nullable=False, default="active") # read, active
    message_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_string = db.Column(db.String(100), unique=True, nullable=False)
    image_path = db.Column(db.String(255), unique=True, nullable=False)
    category = db.Column(db.String(20), nullable=False)
    post_title = db.Column(db.String(255), nullable=False)
    post_description = db.Column(db.String(1000), nullable=True)
    project_link = db.Column(db.String(300), nullable=True)
    post_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)



class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    client_work = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(300), nullable=False)
    testimonial_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    state = db.Column(db.String(20), nullable=False, default="inactive")# active, inactive


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    
    def __repr__(self):
        return f"{self.full_name} / {self.password}"









