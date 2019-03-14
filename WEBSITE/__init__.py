from flask import Flask

app = Flask(__name__)
app.secret_key = '5de42b8b53de04dc8f1172a7fd96b2a3'
from WEBSITE import routes
