from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = '865dccc4db9e2bf50d0acb10877a06e7'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mensa.db'

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'
login_manager.login_message = 'Faça login para acessar esta página'

from comunidademensa import routes