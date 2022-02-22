from config import BaseConfig
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager


def create_blueprints():
    from .views import blueprint_app
    from app.user import blueprint_user
    app.register_blueprint(blueprint_app)
    app.register_blueprint(blueprint_user, url_prefix="/user")


app = Flask(__name__)
app.config.from_object(BaseConfig)

csrf = CSRFProtect(app)

db = SQLAlchemy()
db.init_app(app)

with app.app_context():
    db.create_all()

mail = Mail(app)

login = LoginManager(app)
login.session_protection = 'strong'

create_blueprints()

login.login_view = 'blueprint_user.login'