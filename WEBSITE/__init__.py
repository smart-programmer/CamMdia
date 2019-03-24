from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os

app = Flask(__name__)

if os.environ.get("SECRET_KEY") and os.environ.get("DATABASE_URI"):
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
else:
    app.config["SECRET_KEY"] = "AAA2002AAA"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlite.db"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USERNAME = 'ahmed.coder.2002@gmail.com'
MAIL_PASSWORD = "EpicCoder_2002"  # os.environ.get("MAIL_PASSWORD")
MAIL_USE_SSL = True
app.config['MAIL_SERVER'] = MAIL_SERVER
app.config['MAIL_PORT'] = MAIL_PORT
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
app.config['MAIL_USE_SSL'] = MAIL_USE_SSL
mail = Mail(app)


from WEBSITE import routes