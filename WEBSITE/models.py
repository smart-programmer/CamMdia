from WEBSITE import db, login_manager
from flask_login import UserMixin
from datetime import datetime

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), unique=False, nullable=False)
    subject = db.Column(db.String(255), unique=False, nullable=True)
    email = db.Column(db.String(255), unique=False, nullable=False)
    content = db.Column(db.String(1000), unique=False, nullable=False)



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_string = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(20), nullable=False)
    post_title = db.Column(db.String(255), nullable=False)
    post_description = db.Column(db.String(600), nullable=True)
    project_link = db.Column(db.String(255), nullable=True)
    post_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)







    


#class User





