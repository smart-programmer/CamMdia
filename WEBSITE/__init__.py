from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os

app = Flask(__name__)
if os.environ.get("online"):
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SECRET_KEY"] = "AAA2002AAA"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../sqlite.db"
    # NOTE: the flask migration moudle/package database url must be relative to the file that will be run when migrating offline which in this case is run.py, that's why in the env file the directory is different then in here.

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USERNAME = 'webdevcompany123@gmail.com'
MAIL_PASSWORD = "almowld123488"  # os.environ.get("MAIL_PASSWORD")
MAIL_USE_SSL = True
app.config['MAIL_SERVER'] = MAIL_SERVER
app.config['MAIL_PORT'] = MAIL_PORT
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
app.config['MAIL_USE_SSL'] = MAIL_USE_SSL
mail = Mail(app)




from WEBSITE import routes